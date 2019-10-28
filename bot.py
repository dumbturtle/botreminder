import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,\
    RegexHandler, ConversationHandler, CallbackQueryHandler

from settings import connect_settings
from settings import settings
from bothandlers.handlers import greet_user, join_user, reminder_add,\
    reminds_list, reminder_add_date, calendar_add_date,\
    calendar_add_day, calendar_add_month, calendar_add_year,\
    calendar_add_hours, calendar_add_minutes, reminder_add_comment,\
    reminder_skip_comment, confirm_remind_for_delete, commit_remind_for_delete,\
    cancel_remind_for_delete, dontknow, unjoin_user
from reminds_handlers import main_reminds_handlers

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='logs/bot.log')


def main():
    mybot = Updater(
        connect_settings.API_KEY,
        request_kwargs=connect_settings.PROXY)
    logging.info(settings.RUN_BOT)
    dp = mybot.dispatcher
    reminder_create = ConversationHandler(
        entry_points=[
            RegexHandler(
                '^(Добавить напоминание)$',
                reminder_add,
                pass_user_data=True)],
        states={
            "reminder_add_date": [
                RegexHandler(
                    '^(Ввести дату)$',
                    calendar_add_date,
                    pass_user_data=True),
                    RegexHandler('^([0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9])$',
                    reminder_add_date,
                    pass_user_data=True)],
            "calendar_add_day": [
                RegexHandler(
                    '^([1-9]|0[0-9]|1[0-9]|2[0-9]|3[0-1])$',
                    calendar_add_day,
                    pass_user_data=True)],
            "calendar_add_month": [
                RegexHandler(
                    '^([1-9]|0[0-9]|1[0-2])$',
                    calendar_add_month, 
                    pass_user_data=True)],
            "calendar_add_year": [
                RegexHandler(
                    '^([0-9][0-9][0-9][0-9])$',
                    calendar_add_year,
                    pass_user_data=True)],
            "calendar_add_hours": [
                RegexHandler(
                    '^([0-9]|[0-2][0-9])$',
                    calendar_add_hours,
                    pass_user_data=True)],
            "calendar_add_minutes": [
                RegexHandler(
                    '^([0-9]|[0-5][0-9])$',
                    calendar_add_minutes,
                    pass_user_data=True)],
            "reminder_add_comment": [
                MessageHandler(
                    Filters.text,
                    reminder_add_comment,
                    pass_user_data=True),
                CommandHandler(
                    'skip',
                    reminder_skip_comment,
                    pass_user_data=True)]
        },
        fallbacks=[
            MessageHandler(
                Filters.text |
                Filters.video |
                Filters.photo |
                Filters.document,
                dontknow,
                pass_user_data=True)]
    )
    reminder_delete = ConversationHandler(
        entry_points=[
            RegexHandler(
                '^(Удалить напоминание)$',
                reminds_list,
                pass_user_data=True)],
        states={
            "confirm_remind_for_delete": [
                RegexHandler(
                    '^([0-9]|[0-9][0-9])$',
                    confirm_remind_for_delete,
                    pass_user_data=True)],
            "commit_remind_for_delete": [
                RegexHandler(
                    '^(Да)$',
                    commit_remind_for_delete,
                    pass_user_data=True)]
        },
        fallbacks=[
            RegexHandler(
                '^(Нет)$',
                cancel_remind_for_delete,
                pass_user_data=True),
            MessageHandler(
                Filters.text |
                Filters.video |
                Filters.photo |
                Filters.document,
                dontknow,
                pass_user_data=True)]
    )
    dp.add_handler(
        CommandHandler(
            "start",
            greet_user,
            pass_user_data=True))
    dp.add_handler(reminder_create)
    dp.add_handler(reminder_delete)
    dp.add_handler(
        RegexHandler(
            '^(Хочу пользоваться!)$',
            join_user,
            pass_user_data=True))
    dp.add_handler(
        RegexHandler(
            '^(Расхотел)$',
            unjoin_user,
            pass_user_data=True))
    dp.add_handler(
        RegexHandler(
            '^(Список напоминаний)$',
            reminds_list,
            pass_user_data=True))
    dp.add_handler(
        MessageHandler(
            Filters.text,
            dontknow,
            pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
