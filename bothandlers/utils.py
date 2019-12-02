import logging
import logging.config
from datetime import datetime, timedelta

from sqlalchemy.exc import SQLAlchemyError

from database.modeldb import ReminderData, User, database_session
from settings import settings

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger('BotApp')


def try_to_commit(session):
    """Try commit to database.

    If data saved to database return True.
    If an error occurs while writing to the database is return False
    and error writting to logfile.

    :param session: database session
    :type session: sqlalchemy.orm.session.Session
    :return: True/False
    :rtype: boolean
    """    
    try:
        session.commit()
        return True
    except SQLAlchemyError:
        logger.error(settings.BOT_ERROR_COMMIT)
        return False


def check_date(user_data):
    """Check date for correctness.
    
    If the date is in the future and the conversion occurred without errors, date is returned.
    If the user passed the date in the past, False is returned.
    If an error occurred during the conversion, error string is returned.

    :param user_data: Containing date and time.
    :type user_data: dict
    :return:Date datetime. 
    :rtype: datetime
    :return:False 
    :rtype:boolen. 
    :return: Error
    :type: string  
    """
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
        logger.error(error)
        return 'Error: {}'.format(error)


def add_user_to_database(telegramm_user_id, first_name, last_name, username, chat_id):
    """Add a new user to the database.
    If the user is in the database, return his data. 
    If the user is not in the database, then add the user to the database.
    If adding a user to the database was successful, return True.
    If adding a user to the database was not successful, return False.
    
    :param telegramm_user_id: Telegram user ID.
    :type telegramm_user_id: int
    :param first_name: Name
    :type first_name: string
    :param last_name: Surname
    :type last_name: string
    :param username: Telegramm username
    :type username: string
    :param chat_id: User telegramm chat ID 
    :type chat_id: int 
    :return: True/False 
    :rtype: boolen 
    :return: Information about user
    :rtype: string
    """
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
    """Delete user from database.
    
    User removed from database, return True
    An error occurred while deleting, return False
    If no user in database, return string 'NO USER'.
    
    :param telegramm_user_id: Telegram user ID
    :type telegramm_user_id: int
    :return: True/False
    :rtype: boolen.
    :return: 'No user'
    :rtype: string 
    """
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
    """Check user in database.
    If the user is in the database, full information about him is returned.
    If no user in database, return string 'NO USER'.
   
    :param telegramm_user_id: Telegram user ID
    :type telegramm_user_id: int
    :return: information_about_user 
    :rtype: string
    :return: None
    :rtype: None
    """
    information_about_user = database_session.query(
        User.first_name
    ).filter(
        User.telegramm_user_id == telegramm_user_id
    ).first()
    return information_about_user if information_about_user is not None else None


def reminder_add_database(telegramm_user_id, comment, date_remind, status):
    """Adding a new reminder to the database.
    
    If reminder add to database, returned True.
    If an error occurred while add reimnder to database, return False.

    :param telegramm_user_id: Telegram user ID
    :type telegramm_user_id: int
    :param comment: Reminder Comment
    :type comment: string
    :param date_remind: Date Reminder
    :type date_remind: datetime
    :param status: Reminder status(Active/Deactive)
    :type status: string
    :return: True/False 
    :rtype: boolen
    """
    user_id = database_session.query(
        User.id
    ).filter(
        User.telegramm_user_id == telegramm_user_id
    ).first()
    information_about_reminder = ReminderData(
        user_id[0], comment, date_remind, status)
    database_session.add(information_about_reminder)
    
    return try_to_commit(database_session)


def reminds_list_database(telegramm_user_id):
    """Returns a list of user reminders.
    
    If redimnder in database, return user reminder information. 
    If reminder list is empty, return None.

    :param telegramm_user_id: Telegram user ID
    :type telegramm_user_id: int
    :return: Information_about_reminder
    :rtype: string. 
    :return: 'No remind'
    :rtype: string
    """
    user_id = database_session.query(
        User.id
    ).filter(
        User.telegramm_user_id == telegramm_user_id
    ).first()
    user_list_reminders = database_session.query(
        ReminderData
    ).filter(
        ReminderData.user_id == user_id[0]
    ).all()
    
    return user_list_reminders if user_list_reminders is not None else 'No remind'


def remind_for_delete_information(remind_id):
    """Return information about reminder for delete.
    
    Returned information about reminder.
    If information of reminder is empty? return 'No remind'
    
    :param remind_id: Remind ID in database.
    :type remind_id: int
    :return: remind
    :rtype: string. 
    :return: 'No remind'
    :rtype: string. 
    """
    remind = database_session.query(
        ReminderData
    ).filter(
        ReminderData.id == remind_id
    ).first()
    
    return remind if remind is not None else 'No remind'


def remind_delete(remind_id):
    """Removing a reminder from the database.

    If reminder deleted from database, return True
    If an error occurred while deleting the reminder from the database, return False.
    If reminder not found in database, return None.
   
    :param remind_id: Remind ID in database.
    :type remind_id: int
    :return: True/False
    :rtype: boolen
    :return: None 
    :rtype: None
    """
    remind = database_session.query(
        ReminderData
    ).filter(
        ReminderData.id == remind_id
    ).first()
    
    if remind is None:
        return None
    database_session.query(
        ReminderData
    ).filter(
        ReminderData.id == remind_id
    ).delete()
    
    return try_to_commit(database_session)


def remind_list_message(list_of_reminds):
    """Generates a message text for the user from of the list reminders.
    
    Return text message for the user of the list reminders.
    
    :param list_of_reminds: User Reminder List.
    :type list_of_reminds: list
    :return: text_message
    :rtype: string
    """
    text_message = ''
    
    for remind in list_of_reminds:
        text_message += settings.REMINDER_LIST_MESSAGE.format(remind.id, remind.date_remind, remind.comment, remind.status)
    
    return text_message
