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
    
    Arguments:
        session - database session
    
    Returns:
        True -- type:boolen. Data saved to database.
        False -- type:boolen. Error while saving data to database. Error is writing to log file.
    """    
    try:
        session.commit()
        return True
    except SQLAlchemyError:
        logger.error(settings.BOT_ERROR_COMMIT)
        return False


def check_date(user_data):
    """Check date for correctness.
    
    Arguments:
        user_data - User data containing time.
    
    Returns:
        Date - type: datetime. If the date is in the future and the conversion occurred without errors, the date is returned.
        False - type:boolen. If the user passed the date in the past.
        Error - type: string. If an error occurred during the conversion. 
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
    If the user is not in the database, then add the user to the database
    
    Arguments:
        telegramm_user_id - Telegram user ID.
        first_name - Name
        last_name - Surname
        username - Telegramm username
        chat_id - User telegramm chat ID  
    
    Returns:
        True - type: boolen. If adding a user to the database was successful.
        False - type: boolen. If adding a user to the database was not successful.
        Information about user - type: string. If the user is in the database, 
            then return information about him.
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
   
    Arguments:
        telegramm_user_id - Telegram user ID.
    
    Returns:
        True - type: boolen. User removed from database
        False - type: boolen. An error occurred while deleting.
        String - type: string. If no user in database, return string 'NO USER'.
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
    """Delete user from database.
   
    Arguments:
        telegramm_user_id - Telegram user ID.
    
    Returns:
        True - type: boolen. User removed from database
        False - type: boolen. An error occurred while deleting.
        String - type: string. If no user in database, return string 'NO USER'.
    """
    information_about_user = database_session.query(
        User.first_name
    ).filter(
        User.telegramm_user_id == telegramm_user_id
    ).first()
    return information_about_user if information_about_user is not None else None


def reminder_add_database(telegramm_user_id, comment, date_remind, status):
    """Adding a new reminder to the database.
   
    Arguments:
        telegramm_user_id - Telegram user ID.
        comment - Reminder Comment.
        date_remind - Date Reminder.
        status - Reminder status(Active/Deactive).
    
    Returns:
        True - type: boolen. Reminder add to database.
        False - type: boolen. An error occurred while add reimnder to database.
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
   
    Arguments:
        telegramm_user_id - Telegram user ID.
         
    Returns:
        Information_about_reminder - type: string. User reminder information.
        No remind - type: string. Reminder list is empty.
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
   
    Arguments:
        remind_id - Remind ID in database.
         
    Returns:
        remind - type: string. Information about reminder.
        No remind - type: string. Information of reminder is empty.
    """
    remind = database_session.query(
        ReminderData
    ).filter(
        ReminderData.id == remind_id
    ).first()
    
    return remind if remind is not None else "No remind"


def remind_delete(remind_id):
    """Removing a reminder from the database.
   
    Arguments:
        remind_id - Remind ID in database.
         
    Returns:a
        True - type: boolen. Reminder deleted from database.
        False - type: boolen. An error occurred while deleting the reminder from the database.
        None  - type: None. Reminder not found in database.
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
   
    Arguments:
        list_of_reminds - User Reminder List.
         
    Returns:
        text_message - type: string. Text message for the user of the list reminders.
    """
    text_message = ''
    
    for remind in list_of_reminds:
        text_message += settings.REMINDER_LIST_MESSAGE.format(remind.id, remind.date_remind, remind.comment, remind.status)
    
    return text_message
