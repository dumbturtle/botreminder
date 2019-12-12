from datetime import datetime, timedelta

from telegram import (
    Bot, InlineKeyboardButton, InlineKeyboardMarkup, Message, ParseMode,
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, error)
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          RegexHandler, Updater)

from bothandlers.keyboards import (remind_confirm_for_delete_keyboard,
                                   remind_list_for_delete_keyboard,
                                   reminder_add_date_keyboard,
                                   reminder_add_digital_period_keyboard,
                                   reminder_keyboard, starting_keyboard)
from bothandlers.utils import (add_user_to_database, check_date, convert_date,
                               day_remaining, delete_user_from_database,
                               get_information_about_user, hour_remaining,
                               logger, minute_remaining, month_remaining,
                               reminder_add_new_to_database, reminder_delete,
                               reminder_get_from_database,
                               reminder_list_from_database,
                               reminders_list_message)
from settings import settings


def greet_user(bot: Bot, update: Update, user_data: dict) -> Message:
    """Welcome function. Called upon message: /start
    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: If the user is in the database, the function sends a 
             welcome message to the user indicating his name or 
             a welcome message with a proposal to be added to 
             the database. 
    """
    if get_information_about_user(update.effective_user.id) is None:
        message_text = settings.JOIN_TEXT
        update.message.reply_text(message_text, reply_markup=starting_keyboard())
    else:
        message_text = settings.JOIN_TEXT_FOR_USER.format(update.effective_user.first_name)
        update.message.reply_text(message_text, reply_markup=reminder_keyboard())


def join_user(bot, update, user_data):
    """The function is adding user in the database.
    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: If the user is not in the database, the function add
             user to database and sends a greet message to the user.
             If an error occurs during adding, an error message 
             is sent to the user. 
    """
    if add_user_to_database(update.effective_user.id,
                            update.effective_user.first_name,
                            update.effective_user.last_name,
                            update.effective_user.username,
                            update.message.chat_id):
        text_message = settings.ADD_USER
    else:
        text_message = settings.ADD_ERROR

    update.message.reply_text(text_message, reply_markup=reminder_keyboard())


def unjoin_user(bot: Bot, update: Update, user_data: dict) -> Message:
    """The function is removing user from the database.
    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: If the user is in the database, the function delete
             user from database and sends a message to the user.
             If an error occurs during deletion, an error message 
             is sent to the user. 
    """
    if delete_user_from_database(update.effective_user.id):
        text_message = settings.REMOVE_USER
    else:
        text_message = settings.ADD_ERROR
        
    update.message.reply_text(text_message, reply_markup=starting_keyboard())


def reminder_add(bot: Bot, update: Update, user_data: dict) -> Message:
    """Initial function to create a reminder.

    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with a request 
             to enter a date. 
    """
    text_message = settings.ENTER_DATE
    update.message.reply_text(text_message, reply_markup=reminder_add_date_keyboard())
    
    return "reminder_add_date"


def predefined_add_date(bot: Bot, update: Update, user_data: dict) -> Message:
    """The function suggests choosing tomorrow's date and after tomorrow.

    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with a request 
             to enter a hours. 
    """
    user_data['date'] = update.message.text
    text_message = settings.ENTER_HOURS
    update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard(hour_remaining(user_data['date']), 23, 10, 1))

    return "manual_add_date_hour"


def manual_add_date(bot: Bot, update: Update, user_data: dict) -> Message:
    """The initial date entry function and sends a message to the user with 
       request to enter a day.

    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with a request 
             to enter a day. 
    """
    text_message = settings.ENTER_YEAR
    start_year = datetime.now().year
    end_year = (datetime.now() + timedelta(days=1095)).year
    update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard(start_year, end_year, 1, 1))
    
    return "manual_add_date_year"


def manual_add_date_year(bot: Bot, update: Update, user_data: dict) -> Message:
    """The function adds year to the dictionary 
       user_data and sends a message to the user with a request to enter hour.

    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with a request 
             to enter a hour. 
    """
    user_data['year'] = update.message.text
    start_month = month_remaining(user_data['year'])
    text_message = settings.ENTER_MONTH
    update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard(start_month, 12, 10, 1))
    
    
    return "manual_add_date_month"


def manual_add_date_month(bot: Bot, update: Update, user_data: dict) -> Message:
    """The function adds month to the dictionary 
       user_data and sends a message to the user with a request to enter year.

    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with a request 
             to enter a month. 
    """
    user_data['month'] = update.message.text
    period_days = day_remaining(user_data)
    text_message = settings.ENTER_DAY
    update.message.reply_text(
        text_message, reply_markup=reminder_add_digital_period_keyboard(
            period_days.get('start'), period_days.get('end'), 10, 1))
    
    return "manual_add_date_day"


def manual_add_date_day(bot: Bot, update: Update, user_data: dict) -> Message:
    """The function adds day to the dictionary 
       user_data and sends a message to the user with a request to enter month.

    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with a request 
             to enter a month. 
    """
    text_message = settings.ENTER_HOURS
    user_data['day'] = update.message.text
    start_hour = hour_remaining('{}-{}-{}'.format(user_data['day'], user_data['month'], user_data['year']))
    update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard(start_hour, 23, 10, 1))
    
    return "manual_add_date_hour"
    

def manual_add_date_hour(bot: Bot, update: Update, user_data: dict) -> Message:
    """The function adds hour to the dictionary 
       user_data and sends a message to the user with a request to enter minute.

    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with a request 
             to enter a minute. 
    """
    user_data['hours'] = update.message.text
    start_minute = minute_remaining(user_data, 5)
    text_message = settings.ENTER_MINUTES
    update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard(start_minute, 59, 10, 5))
    
    return "manual_add_date_minute"


def manual_add_date_minute(bot: Bot, update: Update, user_data: dict) -> Message:
    """The function adds minutes to the dictionary, 
       checks the correct date and time and sends a message 
       to the user asking him to enter a comment.

    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with a request 
             to enter a comment. 
    """
    user_data['minutes'] = update.message.text
    
    date_after_convert = convert_date(user_data)     

    if isinstance(date_after_convert, datetime) and check_date(date_after_convert):
        user_data['date'] = date_after_convert
        text_message = settings.ENTER_COMMENT
        update.message.reply_text(text_message, reply_markup=ReplyKeyboardRemove())
        return "reminder_add_comment"
    else:
        text_message = settings.INVALID_DATE_OR_TIME
        update.message.reply_text(text_message, reply_markup=reminder_add_date_keyboard())
        return "reminder_add_date"


def reminder_add_comment(bot: Bot, update: Update, user_data: dict) -> Message:
    """The function adds a comment to the dictionary,
       and adds a reminder to the database.
    
    The function sends a message to the user with reminder parameters and 
    ends the dialog or sends an error and asks to enter reminder parameters.
    
    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with reminer or error. 
    """
    user_data['comment'] = update.message.text
    if reminder_add_new_to_database(update.effective_user.id, 
                                    user_data['comment'], 
                                    user_data['date'], 
                                    settings.REMINDER_STATUS_ON_ADD):
            text_message = settings.COMMIT_WITH_COMMENT.format(
                user_data["date"], user_data["comment"], settings.TRUE_COMMIT_STATUS)
            update.message.reply_text(text_message, reply_markup=reminder_keyboard())
            return ConversationHandler.END
    else:
        text_message = settings.ADD_ERROR
        update.message.reply_text(text_message, reply_markup=reminder_add_date_keyboard())
        return "reminder_add_date"
    
    

def reminder_skip_comment(bot: Bot, update: Update, user_data: dict) -> Message:
    """The function skips adding a comment to the reminder 
       and writes reminders to the database.
    
    The function sends a message to the user with reminder parameters and 
    ends the dialog or sends an error and asks to enter reminder parameters.
    
    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with reminer or error. 
    """
    user_data['comment'] = settings.NO_COMMENT
    if reminder_add_new_to_database(update.effective_user.id, 
                                    user_data['comment'], 
                                    user_data['date'], 
                                    settings.REMINDER_STATUS_ON_ADD):
            text_message = settings.COMMIT_WITH_COMMENT.format(
                user_data["date"], user_data["comment"], settings.TRUE_COMMIT_STATUS)
            text_message = settings.COMMIT_WITHOUT_COMMENT
            update.message.reply_text(text_message, reply_markup=reminder_keyboard())
            return ConversationHandler.END
    else:
        text_message = settings.ADD_ERROR
        update.message.reply_text(text_message, reply_markup=reminder_add_date_keyboard())
        return "reminder_add_date" 
    

def reminder_list(bot: Bot, update: Update, user_data: dict) -> Message:
    """The function forms a list of reminders and sends it to the user.
 
    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with list of reminers. 
    """
    text_message = ''
    list_reminders = reminder_list_from_database(update.effective_user.id)
    text_message = reminders_list_message(list_reminders)
    update.message.reply_text(text_message, reply_markup=reminder_keyboard())
 

def reminder_deleting_list(bot: Bot, update: Update, user_data: dict) -> Message:
    """The function forms a list of reminders for deleting
       and sends it to the user.
 
    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with list of reminers. 
    """
    list_reminders = reminder_list_from_database(update.effective_user.id)
    keys_list_reminder = [f'{reminder.get("id")}' for reminder in list_reminders]
    text_message = reminders_list_message(list_reminders)
    update.message.reply_text(text_message)
    update.message.reply_text(settings.CHOOSE_REMIND_FOR_DELETE, reply_markup=remind_list_for_delete_keyboard(keys_list_reminder))
    
    return "reminder_confirm_for_delete"
    
    
def reminder_confirm_for_delete(bot: Bot, update: Update, user_data: dict) -> Message:
    """The function asks for confirmation to delete the reminder.
 
    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with list of reminers. 
    """
    user_data["number_reminder_for_delete"] = update.message.text
    reminder_for_delete = reminder_get_from_database(user_data["number_reminder_for_delete"])
    if reminder_for_delete.get('id') is None:
        text_message = settings.NO_REMIND
        update.message.reply_text(text_message, reply_markup=reminder_keyboard())
    else:
        description_reminder_for_delete = settings.REMINDER_LIST_MESSAGE.format(reminder_for_delete.get('id'), 
                                                                       reminder_for_delete.get('date_remind'), 
                                                                       reminder_for_delete.get('comment'), 
                                                                       reminder_for_delete.get('status'))
        text_message = settings.CONFIRM_REMIND_FOR_DELETE.format(description_reminder_for_delete)
        update.message.reply_text(text_message, reply_markup=remind_confirm_for_delete_keyboard())
        
        return "reminder_commit_for_delete"


def reminder_commit_for_delete(bot: Bot, update: Update, user_data:dict) -> Message:
    """In case of successful removal of the reminder from the database, 
       the function generates a message to the user with confirmation; 
       if the removal was unsuccessful, an error message is sent.
 
    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with 
             confirmation of deletion or error.. 
    """
    if reminder_delete(user_data["number_reminder_for_delete"]):
        text_message = settings.REMOVE_REMIND_FOR_DELETE
    else:
        text_message = settings.ADD_ERROR
    
    update.message.reply_text(text_message, reply_markup=reminder_keyboard())
    
    return ConversationHandler.END

def reminder_cancel_for_delete(bot, update, user_data):
    """The function sends a message to the user in case of 
       cancellation of the reminder.
 
    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user with cancellation. 
    """
    update.message.reply_text(settings.CANCEL_REMIND_FOR_DELETE, reply_markup=reminder_keyboard())
    
    return ConversationHandler.END


def dontknow(bot: Bot, update: Update, user_data: dict) -> Message:
    """The function interrupts the dialogue and sends a message to the 
       user about the unknown command.

    :param bot: Bot
    :param update: Update
    :param user_data: User data
    :return: The function sends a message to the user about 
             the unknown command. 
    """
    update.message.reply_text(settings.DONTKNOW_TEXT, reply_markup=reminder_keyboard())
    
    return ConversationHandler.END
