
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

from database.modeldb import database_session, User, Reminder_data


def check_date(date):
    today_date = datetime.today()
    try:
        date_for_check = datetime.strptime(date, "%d-%m-%Y %H:%M")
        if date_for_check > today_date:
            return date_for_check
        else:
            return 'False: date in paste'
    except ValueError as error:
        return 'Error:{}'.format(error)


def add_user_to_database(telegramm_user_id, first_name, last_name, username,\
                                                                   chat_id):
    information_about_user = database_session.\
        query(User).\
        filter(User.telegramm_user_id == telegramm_user_id).\
        all()
    if information_about_user is not None:
        information_about_user = User(
            telegramm_user_id,
            first_name, 
            last_name, 
            username, 
            chat_id)
        database_session.add(information_about_user)
        try:
            database_session.commit()
            return 'Commited'
        except SQLAlchemyError:
            return 'Error'
    return information_about_user


def delete_user_from_database(telegramm_user_id):
    information_about_user = database_session.query(User).\
        filter(User.telegramm_user_id == telegramm_user_id).\
        all()
    if information_about_user is None:
        return 'No user'
    database_session.query(User).filter(
        User.telegramm_user_id == telegramm_user_id).delete()
    try:
        database_session.commit()
        return 'Commited'
    except SQLAlchemyError:
        return 'Error'


def check_user_in_database(telegramm_user_id):
    information_about_user = database_session.query(User.first_name).\
        filter(User.telegramm_user_id == telegramm_user_id).\
        first()
    if information_about_user is None:
        return 'No user'
    return information_about_user


def reminder_add_database(telegramm_user_id, comment, date_remind, status):
    user_id = database_session.query(User.id).\
        filter(User.telegramm_user_id == telegramm_user_id).\
        first()
    information_about_reminder = Reminder_data(
        user_id[0],
        comment,
        date_remind,
        status)
    database_session.add(information_about_reminder)
    try:
        database_session.commit()
        return 'Commited'
    except SQLAlchemyError:
        return 'Error'


def reminds_list_database(telegramm_user_id):
    user_id = database_session.query(User.id).\
        filter(User.telegramm_user_id == telegramm_user_id).\
        first()
    information_about_reminder = database_session.\
        query(Reminder_data).\
        filter(Reminder_data.user_id == user_id[0]).\
        all()
    if information_about_reminder is None:
        return 'No remind'
    return information_about_reminder


def remind_list_for_delete(remind_id):
    remind = database_session.\
        query(Reminder_data).\
        filter(Reminder_data.id == remind_id).\
        first()
    return remind if remind is not None else "No remind"


def remind_delete(remind_id):
    remind = database_session.\
        query(Reminder_data).\
        filter(Reminder_data.id == remind_id).\
        first()
    if remind is None:
        return 'No remind'
    database_session.query(Reminder_data).\
        filter(Reminder_data.id == remind_id).\
        delete()
    try:
        database_session.commit()
        return 'Commited'
    except SQLAlchemyError:
        return 'Error'
