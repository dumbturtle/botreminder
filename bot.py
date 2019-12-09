from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          RegexHandler, Updater)

from bothandlers.handlers import (manual_add_date, manual_add_date_day,
                                 manual_add_date_hour, manual_add_date_minute,
                                 manual_add_date_month, manual_add_date_year,
                                  reminder_confirm_for_delete,
                                  reminder_commit_for_delete, 
                                  reminder_cancel_for_delete, dontknow,
                                  greet_user, join_user, logger, reminder_add,
                                  reminder_add_comment, reminder_skip_comment,
                                  reminder_list, unjoin_user, predefined_add_date,
                                  reminder_deleting_list)
from settings import connect_settings, settings


def main():
    mybot = Updater(connect_settings.API_KEY, request_kwargs={'proxy_url': connect_settings.PROXY, 'urllib3_proxy_kwargs': connect_settings.PROXY_ACCOUNT})
    dp = mybot.dispatcher
    logger.info(settings.BOT_RUN)
    reminder_create = ConversationHandler(
        entry_points=[
            RegexHandler('^(Добавить напоминание)$', reminder_add, pass_user_data=True)
            ],
        states={
            "reminder_add_date": [
                RegexHandler('^(Ввести дату)$', manual_add_date, pass_user_data=True),
                RegexHandler('^([0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9])$', predefined_add_date, pass_user_data=True)
                ],
             "manual_add_date_year": [
                RegexHandler('^([0-9][0-9][0-9][0-9])$', manual_add_date_year, pass_user_data=True)
                ],
             "manual_add_date_month": [
                RegexHandler('^([1-9]|0[0-9]|1[0-2])$', manual_add_date_month, pass_user_data=True)
                ],
             "manual_add_date_day": [
                RegexHandler('^([1-9]|0[0-9]|1[0-9]|2[0-9]|3[0-1])$', manual_add_date_day, pass_user_data=True)
                ],
             "manual_add_date_hour": [
                RegexHandler('^([0-9]|[0-2][0-9])$', manual_add_date_hour, pass_user_data=True)
                ],
             "manual_add_date_minute": [
                RegexHandler('^([0-9]|[0-5][0-9])$', manual_add_date_minute, pass_user_data=True)
                ],
            "reminder_add_comment": [
                MessageHandler(Filters.text, reminder_add_comment, pass_user_data=True),
                CommandHandler('skip', reminder_skip_comment, pass_user_data=True)
                ]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document, dontknow, pass_user_data=True)
            ]
    )
    reminder_delete = ConversationHandler(
        entry_points=[
            RegexHandler('^(Удалить напоминание)$', reminder_deleting_list, pass_user_data=True)
            ],
        states={
            'reminder_confirm_for_delete': [
                RegexHandler('^([0-9]|[0-9][0-9])$', reminder_confirm_for_delete, pass_user_data=True)
                ],
            'reminder_commit_for_delete': [
                RegexHandler('^(Да)$', reminder_commit_for_delete, pass_user_data=True)
                ]
        },
        fallbacks=[
            RegexHandler('^(Нет)$', reminder_cancel_for_delete, pass_user_data=True),
            MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document, dontknow, pass_user_data=True)
            ]
    )
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(reminder_create)
    dp.add_handler(reminder_delete)
    dp.add_handler(RegexHandler('^(Хочу пользоваться!)$',join_user, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Расхотел)$', unjoin_user, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Список напоминаний)$', reminder_list, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, dontknow, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
