import logging

from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

from database.modeldb import database_session, User, Reminder_data
from settings import settings

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger('BotApp')


def try_to_commit(session):
    try:
        session.commit()
        return True
    except SQLAlchemyError:
        logger.error(settings.BOT_ERROR_COMMIT)
        return False


def check_date(user_data):
    today_date = datetime.today()
    
    if "day" in user_data:
        user_data['date'] = '{}-{}-{} {}:{}'.format(
            user_data["day"], user_data["month"], user_data["year"],
            user_data["hours"], user_data["minutes"])
    else:
        user_data['date'] = '{} {}:{}'.format(user_data["date"], user_data["hours"], user_data["minutes"])
    try:
        date_for_check = datetime.strptime(user_data["date"], "%d-%m-%Y %H:%M")
        if date_for_check > today_date:
            return date_for_check
            
        else:
            return False
    except ValueError as error:
        return 'Error: {}'.format(error)


def add_user_to_database(telegramm_user_id, first_name, last_name, username, chat_id):
    information_about_user = database_session.query(
        User
    ).filter(
        User.telegramm_user_id == telegramm_user_id
    ).all()
    
    if information_about_user is not None:
        information_about_user = User(telegramm_user_id, first_name, last_name, username, chat_id)
        database_session.add(information_about_user)
        return try_to_commit(database_session)
    
    return information_about_user


def delete_user_from_database(telegramm_user_id):
    information_about_user = database_session.query(
        User
    ).filter(
        User.telegramm_user_id == telegramm_user_id
    ).all()
    
    if information_about_user is None:
        return settings.BOT_NO_USER
    database_session.query(
        User
    ).filter(
        User.telegramm_user_id == telegramm_user_id
    ).delete()
    
    return try_to_commit(database_session)


def check_user_in_database(telegramm_user_id):
    information_about_user = database_session.query(
        User.first_name
    ).filter(
        User.telegramm_user_id == telegramm_user_id
    ).first()
    return information_about_user if information_about_user is not None else None


def reminder_add_database(telegramm_user_id, comment, date_remind, status):
    user_id = database_session.query(
        User.id
    ).filter(
        User.telegramm_user_id == telegramm_user_id
    ).first()
    information_about_reminder = Reminder_data(
        user_id[0], comment, date_remind, status)
    database_session.add(information_about_reminder)
    
    return try_to_commit(database_session)


def reminds_list_database(telegramm_user_id):
    user_id = database_session.query(
        User.id
    ).filter(
        User.telegramm_user_id == telegramm_user_id
    ).first()
    information_about_reminder = database_session.query(
        Reminder_data
    ).filter(
        Reminder_data.user_id == user_id[0]
    ).all()
    
    return information_about_reminder if information_about_reminder is not None else 'No remind'


def remind_list_for_delete(remind_id):
    remind = database_session.query(
        Reminder_data
    ).filter(
        Reminder_data.id == remind_id
    ).first()
    
    return remind if remind is not None else "No remind"


def remind_delete(remind_id):
    remind = database_session.query(
        Reminder_data
    ).filter(
        Reminder_data.id == remind_id
    ).first()
    
    if remind is None:
        return None
    database_session.query(
        Reminder_data
    ).filter(
        Reminder_data.id == remind_id
    ).delete()
    
    return try_to_commit(database_session)


def remind_list_message(list_of_reminds):
    text_message = ''
    
    for remind in list_of_reminds:
        text_message += settings.REMINDER_LIST_MESSAGE.format(remind.id, remind.date_remind, remind.comment, remind.status)
    
    return text_message