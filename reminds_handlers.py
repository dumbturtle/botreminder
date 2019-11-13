
import logging
import logging.config
import schedule
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from telegram import Bot, utils

from settings import connect_settings, settings
from database.modeldb import database_session, User, Reminder_data

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger('RemindApp')


def check_time_reminder():
    reminders_list = database_session.query(
        Reminder_data
    ).filter(
        Reminder_data.status == 'active'
    ).all()
    
    for reminder in reminders_list:
        logger.info("Проверено напоминание: {}-{}-{}".format(reminder.user_id, reminder.date_remind, reminder.comment))
        if reminder.date_remind.strftime("%d-%m-%Y %H:%M") == ((datetime.now() + timedelta(hours=3)).strftime("%d-%m-%Y %H:%M")):
            sending_notification_reminder(reminder.user_id, reminder.date_remind, reminder.comment)
            change_reminder_status(reminder.id)


def sending_notification_reminder(user_id, reminder_date, comment):
    user_information = database_session.query(
        User
    ).filter(
        User.id == user_id
    ).first()
    
    bot_proxy = utils.request.Request(proxy_url=connect_settings.PROXY, urllib3_proxy_kwargs=connect_settings.PROXY_ACCOUNT)
    reminder_bot = Bot(token=connect_settings.API_KEY, equest=bot_proxy)
    message_text = settings.REMIND_MESSAGE_TEXT.format(reminder_date, comment)
    reminder_bot.sendMessage(chat_id=user_information.chat_id, text=message_text)


def change_reminder_status(remind_id):
    database_session.query(
        Reminder_data
    ).filter(
        Reminder_data.id == remind_id
    ).update({'status': 'deactive'})   
    
    try:
        database_session.commit()
    except SQLAlchemyError:
        logger.error("Commit error")


def main_reminds_handlers():
    logger.info('Reminds Handlers Start')
    schedule.every().minute.at(":01").do(check_time_reminder)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main_reminds_handlers()
