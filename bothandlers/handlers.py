import logging
from datetime import datetime
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode,\
    error, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,\
    RegexHandler, ConversationHandler, CallbackQueryHandler

from settings import settings

from bothandlers.keyboards import starting_keyboard, reminder_keyboard,\
    reminder_add_day_keyboard, reminder_add_digital_period_keyboard,\
    remind_list_for_delete_keyboard, remind_confirm_for_delete_keyboard
from bothandlers.utils import check_date, add_user_to_database,\
    check_user_in_database, reminder_add_database, reminds_list_database,\
    remind_list_for_delete, remind_delete, delete_user_from_database,\
    remind_list_message


def greet_user(bot, update, user_data):
    check_user = check_user_in_database(update.effective_user.id)

    if check_user == "No user":
        message_text = settings.JOIN_TEXT
        update.message.reply_text(message_text, reply_markup=starting_keyboard())
    else:
        message_text = settings.JOIN_TEXT_FOR_USER.format(check_user[0])
        update.message.reply_text(message_text, reply_markup=reminder_keyboard())


def join_user(bot, update, user_data):
    commit_status = add_user_to_database(
        update.effective_user.id, update.effective_user.first_name,
        update.effective_user.last_name, update.effective_user.username,
        update.message.chat_id)
    if commit_status:
        text_message = settings.ADD_USER
    elif not commit_status:
        text_message = settings.ADD_ERROR
    else:
        commit_status = commit_status[0].first_name
        text_message = settings.ALREADY_EXISTS_USER.format(commit_status)
    update.message.reply_text(text_message, reply_markup=reminder_keyboard())


def unjoin_user(bot, update, user_data):
    commit_status = delete_user_from_database(update.effective_user.id)
    
    if commit_status:
        text_message = settings.REMOVE_USER
    elif not commit_status:
        text_message = settings.ADD_ERROR
    else:
        text_message = settings.NO_USER
    
    update.message.reply_text(text_message, reply_markup=starting_keyboard())


def reminder_add(bot, update, user_data):
    text_message = settings.ENTER_DATE
    update.message.reply_text(text_message, reply_markup=reminder_add_day_keyboard())
    
    return "reminder_add_date"


def reminds_list(bot, update, user_data):
    text_message = ''
    list_of_reminds = reminds_list_database(update.effective_user.id)
    keys_list_of_reminds = [f'{key.id}' for key in list_of_reminds]
    update.message.reply_text(settings.REMINDER_ALL_LIST_MESSAGE, reply_markup=reminder_keyboard())
    
    if update.message.text == settings.REMINDER_ALL_LIST_MESSAGE:
        text_message = remind_list_message(list_of_reminds)
        update.message.reply_text(text_message, reply_markup=reminder_keyboard())
        
        return ConversationHandler.END
    else:
        for remind in list_of_reminds:
            text_message = remind_list_message(list_of_reminds)
        
        update.message.reply_text(text_message)
        update.message.reply_text(settings.CHOOSE_REMIND_FOR_DELETE, reply_markup=remind_list_for_delete_keyboard(keys_list_of_reminds))
    
        return "confirm_remind_for_delete"


def reminder_add_date(bot, update, user_data):
    user_data['date'] = update.message.text
    text_message = settings.ENTER_HOURS
    update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard(0, 23, 10, 1))
    
    return "calendar_add_hours"


def calendar_add_date(bot, update, user_data):
    text_message = settings.ENTER_DAY
    update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard(1, 31, 10, 1))
    
    return "calendar_add_day"


def calendar_add_day(bot, update, user_data):
    text_message = settings.ENTER_MONTH
    user_data['day'] = update.message.text
    update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard(1, 12, 10, 1))
    
    return "calendar_add_month"


def calendar_add_month(bot, update, user_data):
    text_message = settings.ENTER_YEAR
    user_data['month'] = update.message.text
    update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard(2019, 2022, 1, 1))
    
    return "calendar_add_year"


def calendar_add_year(bot, update, user_data):
    user_data['year'] = update.message.text
    text_message = settings.ENTER_HOURS
    update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard(0, 23, 10, 1))
    
    return "calendar_add_hours"


def calendar_add_hours(bot, update, user_data):
    user_data['hours'] = update.message.text
    text_message = settings.ENTER_MINUTES
    update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard(0, 59, 10, 5))
    
    return "calendar_add_minutes"


def calendar_add_minutes(bot, update, user_data):
    user_data['minutes'] = update.message.text
    date_status = check_date(user_data)
    
    if isinstance(date_status, datetime):
        user_data['date'] = date_status
        text_message = settings.ENTER_COMMENT
        update.message.reply_text(text_message, reply_markup=ReplyKeyboardRemove())
        return "reminder_add_comment"
    elif not date_status:
        text_message = settings.INVALID_DATE_OR_TIME.format(date_status)
    else:
        text_message = settings.ADD_ERROR
        logging.error(user_data) 
        
    update.message.reply_text(text_message, reply_markup=reminder_add_day_keyboard())
    
    return "reminder_add_date"


def reminder_add_comment(bot, update, user_data):
    user_data['comment'] = update.message.text
    commit_status = reminder_add_database(update.effective_user.id, user_data['comment'], user_data['date'], settings.REMINDER_STATUS_ON_ADD)
    text_message = settings.COMMIT_WITH_COMMENT.format(user_data["date"], user_data["comment"], commit_status)
    update.message.reply_text(text_message, reply_markup=reminder_keyboard())
    
    return ConversationHandler.END


def reminder_skip_comment(bot, update, user_data):
    text_message = settings.COMMIT_WITHOUT_COMMENT
    user_data['comment'] = settings.NO_COMMENT
    update.message.reply_text(text_message, reply_markup=reminder_keyboard())
    
    return ConversationHandler.END


def confirm_remind_for_delete(bot, update, user_data):
    user_data["number_remind_for_delete"] = update.message.text
    remind_for_delete = remind_list_for_delete(user_data["number_remind_for_delete"])
    
    if remind_for_delete == "No remind":
        text_message = settings.NO_REMIND
        update.message.reply_text(text_message, reply_markup=reminder_keyboard())
    else:
        full_remind_for_delete = settings.REMINDER_LIST_MESSAGE.format(remind_for_delete.id, remind_for_delete.date_remind, remind_for_delete.comment, remind_for_delete.status)
        text_message = settings.CONFIRM_REMIND_FOR_DELETE.format(full_remind_for_delete)
        update.message.reply_text(text_message, reply_markup=remind_confirm_for_delete_keyboard())
        
        return "commit_remind_for_delete"


def commit_remind_for_delete(bot, update, user_data):
    commit_status = remind_delete(user_data["number_remind_for_delete"])

    if commit_status:
        text_message = settings.REMOVE_REMIND_FOR_DELETE
    elif not commit_status:
        text_message = settings.ADD_ERROR
    else:
        text_message = settings.NO_REMIND
    
    update.message.reply_text(text_message, reply_markup=reminder_keyboard())
    
    return ConversationHandler.END


def cancel_remind_for_delete(bot, update, user_data):
    update.message.reply_text(settings.CANCEL_REMIND_FOR_DELETE, reply_markup=reminder_keyboard())
    
    return ConversationHandler.END


def dontknow(bot, update, user_data):
    update.message.reply_text(settings.DONTKNOW_TEXT, reply_markup=reminder_keyboard())
    
    return ConversationHandler.END
