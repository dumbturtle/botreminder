
import logging
import schedule
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from telegram import Bot, utils

import settings.connect_settings
import settings.settings 
from database.db import database_session, User, Reminder_data


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='logs\reminds_handlers.log')
bot_proxy = utils.request.Request(proxy_url=connect_settings.PROXY_REMINDS_HANDLERS_PROXY,
                                  urllib3_proxy_kwargs=connect_settings.PROXY_REMINDS_HANDLERS_ACCOUNT)
reminder_bot = Bot(token=connect_settings.API_KEY, request=bot_proxy)


def check_time_reminder():
    reminders_list = database_session.query(Reminder_data).filter(Reminder_data.status == 'active').all()
    for reminder in reminders_list:
        if reminder.date_remind.strftime("%d-%m-%Y %H:%M") == datetime.now().strftime("%d-%m-%Y %H:%M"):
            sending_notification_reminder(reminder.user_id, reminder.date_remind, reminder.comment)
            change_reminder_status(reminder.id)
            logging.warning(settings.REMIND_RUNNINGOUT.format(reminder.id, reminder.date_remind))
        else:
            logging.info(settings.REMIND_CHECK.format(reminder.id, reminder.date_remind))


def sending_notification_reminder(user_id, reminder_date, comment):
    user_information = database_session.query(User).filter(User.id == user_id).first()
    message_text = settings.REMIND_MESSAGE_TEXT.format(reminder_date, comment)
    reminder_bot.sendMessage(chat_id=user_information.chat_id, text=message_text)


def change_reminder_status(remind_id):
    database_session.query(Reminder_data).filter(Reminder_data.id == remind_id).update({'status': 'deactive'})
    try:
        database_session.commit()
        return 'Commited'
    except SQLAlchemyError:
        return 'Error'


def main():
    schedule.every(50).seconds.do(check_time_reminder)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
