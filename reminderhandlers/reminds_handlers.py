import logging
import logging.config
from datetime import datetime, timedelta

import schedule
from sqlalchemy.exc import SQLAlchemyError
from telegram import Bot, utils

from database.modeldb import ReminderData, User, database_session
from settings import connect_settings, settings

logging.config.fileConfig('settings/logging.cfg')
logger = logging.getLogger('RemindApp')


def check_time_reminder() -> None:
    """The function check base with reminders. 
       If there is a match in time, the message sending 
       function is called.
    """
    reminders_list = database_session.query(
        ReminderData
    ).filter(
        ReminderData.status == 'active'
    ).all()
    
    for reminder in reminders_list:
        logger.info("Проверено напоминание: {}-{}-{}".format(reminder.user_id, reminder.date_remind, reminder.comment))
        if reminder.date_remind.strftime("%d-%m-%Y %H:%M") == ((datetime.now() + timedelta(hours=3)).strftime("%d-%m-%Y %H:%M")):
            sending_notification_reminder(reminder.user_id, reminder.date_remind, reminder.comment)
            change_reminder_status(reminder.id)


def sending_notification_reminder(user_id: int, reminder_date: datetime, comment: str) -> None:
    """The function sends a message with reminder to the user.
    """
    user_information = database_session.query(
        User
    ).filter(
        User.id == user_id
    ).first()
    
    bot_proxy = utils.request.Request(proxy_url=connect_settings.PROXY, urllib3_proxy_kwargs=connect_settings.PROXY_ACCOUNT)
    reminder_bot = Bot(token=connect_settings.API_KEY, equest=bot_proxy)
    message_text = settings.REMIND_MESSAGE_TEXT.format(reminder_date, comment)
    reminder_bot.sendMessage(chat_id=user_information.chat_id, text=message_text)


def change_reminder_status(remind_id: int) -> None:
    """The function changes the status in the database 
       on "disable" after sending a message with a reminder.
    """
    database_session.query(
        ReminderData
    ).filter(
        ReminderData.id == remind_id
    ).update({'status': 'deactive'})   
    
    try:
        database_session.commit()
    except SQLAlchemyError:
        logger.error("Commit error")


def main_reminds_handlers() -> None:
    """The function launches the database 
       check function every minute.
    """
    logger.info('Reminds Handlers Start')
    schedule.every().minute.at(":01").do(check_time_reminder)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main_reminds_handlers()
