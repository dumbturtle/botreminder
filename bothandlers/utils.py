import calendar
import logging
import random
import logging.config
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

from sqlalchemy.exc import SQLAlchemyError

from database.modeldb import ReminderData, User, database_session
from settings import settings

logging.config.fileConfig('settings/logging.cfg')
logger = logging.getLogger('BotApp')


def try_to_commit(session) -> bool:
    """Try commit to database.

    :param session: database session
    :return: If data saved to database return True. If an error occurs while writing 
             to the database is return False and error writting to logfile.
    """    
    try:
        session.commit()
        return True
    except SQLAlchemyError:
        logger.error(settings.BOT_ERROR_COMMIT)
        return False

def convert_date(user_data: dict) -> Optional[datetime]:
    """Convert date from dictionary to datetime object.
    
    :param user_data: The date and time to trigger reminders.
    :return: In case of a successful conversion, contains the date and time in a datetime.
    """
    if 'day' in user_data:
        user_data['date'] = '{}-{}-{} {}:{}'.format(
            user_data['day'], user_data['month'], user_data['year'],
            user_data['hours'], user_data['minutes'])
    else:
        user_data['date'] = '{} {}:{}'.format(user_data['date'], user_data['hours'], user_data['minutes'])
    try:
        date_for_convert = datetime.strptime(user_data['date'], '%d-%m-%Y %H:%M')
        return date_for_convert
    except ValueError as error:
        logger.error(error)
        return None


def check_date(redimnder_date: datetime)-> bool:
    """Checks that the time and date in the future.
    
    If the date is in the future, date is returned.
    If the user passed the date in the past, None is returned.

    :param redimnder_date: Containing date and time.
    :return: If future time returns time and date. 
    """
    today_date = datetime.today()

    return True if redimnder_date > today_date else False


def get_information_about_user(telegramm_user_id: int)-> Optional[Dict[str, Union[str, int]]]:   
    """ Get information about user from database.
    
    :param telegramm_user_id: Telegram user ID
    :return: Returns a dictionary with user data from a database
    """         
    information_from_database = database_session.query(
        User
    ).filter(
        User.telegramm_user_id == telegramm_user_id
    ).first()
    if information_from_database is not None:
        information_about_user = {'telegramm_user_id' : information_from_database.telegramm_user_id,
                                  'first_name' : information_from_database.first_name,
                                  'last_name' : information_from_database.last_name,
                                  'username' : information_from_database.username,
                                  'chat_id' : information_from_database.chat_id,
                                 }
        return information_about_user


def add_user_to_database(telegramm_user_id: int, first_name: str, last_name: str, username: str, chat_id: int) -> bool:
    """Add a new user to the database.
     
    :param telegramm_user_id: Telegram user ID.
    :param first_name: User Name
    :param last_name: User Surname
    :param username: Login in Telegramm
    :param chat_id: User telegramm chat ID 
    :return: If the user is not in the database, then add the user to the database. If adding a user to 
             the database was successful, return True. If adding a user to the database was not successful, return False.
    """
    if get_information_about_user(telegramm_user_id) is not None:
        return False
    information_about_user = User(telegramm_user_id, first_name, 
                                  last_name, username, chat_id)
    database_session.add(information_about_user)
    
    return try_to_commit(database_session)
    

def delete_user_from_database(telegramm_user_id: int) -> bool:
    """Delete user from database.
    
    User removed from database, return True
    An error occurred while deleting, return False
    If no user in database, return string 'NO USER'.
    
    :param telegramm_user_id: Telegram user ID
    :return:  If the user deletion from the database is successful, 
              returns True. If no user in database or an error 
              occurred while deleting, returns False.

    """
    if get_information_about_user(telegramm_user_id) is None:
        return False
    database_session.query(
        User
    ).filter(
        User.telegramm_user_id == telegramm_user_id
    ).delete()
    
    return try_to_commit(database_session)

def reminder_add_new_to_database(telegramm_user_id: int, comment: str, date_remind: datetime, status: str) -> bool:
    """Adding a new reminder to the database.
    
    If reminder add to database, returned True.
    If an error occurred while add reimnder to database, return False.

    :param telegramm_user_id: Telegram user ID
    :param comment: User comment on reminder.
    :param date_remind: Date reminder
    :param status: Reminder status(Active/Deactive)
    :return: Returns True if a reminder is added to the database. Returns 
                     False if an error occurred while adding a reminder 
                     to the database. 
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


def reminder_list_from_database(telegramm_user_id: int) -> List[Optional[Dict[str, Union[str, int, datetime]]]]:
    """Returns a list of user reminders.

    :param telegramm_user_id: Telegram user ID
    :return: If there are reminders in the database, the list
             with dict of user reminders is returned; if there are no 
             reminders, it is returned None.
    """
    user_id = database_session.query(
        User.id
    ).filter(
        User.telegramm_user_id == telegramm_user_id
    ).first()
    list_reminder_database = database_session.query(
        ReminderData
    ).filter(
        ReminderData.user_id == user_id[0]
    ).all()
    user_list_reminder = [ {'id' : reminder.id, 
                            'user_id' : reminder.user_id,
                            'comment' : reminder.comment,
                            'date_remind' : reminder.date_remind,
                            'status' : reminder.status} for reminder in list_reminder_database]
    return user_list_reminder

def reminder_get_from_database(remind_id: int) -> Dict[str, Union[str, int, datetime, None]]:
    """Return information about reminder for delete.
    
    :param remind_id: Remind ID in database.
    :return:  Returned information about user reminder in Dict formate.
    """
    
    reminder_from_database = database_session.query(
        ReminderData
    ).filter(
        ReminderData.id == remind_id
    ).first()
    if reminder_from_database is not None:
        reminder = {
                    'id' : reminder_from_database.id, 
                    'user_id' : reminder_from_database.user_id,
                    'comment' : reminder_from_database.comment,
                    'date_remind' : reminder_from_database.date_remind,
                    'status' : reminder_from_database.status
                    }
    else:
        reminder = {
                    'id' : None
                    }
    return reminder


def reminder_delete(reminder_id: int) -> bool:
    """Removing a reminder from the database.
   
    :param reminder_id: Remind ID in database.
    :return: Returns True if the reminder is deleted from the database. Returns 
                     False if an error occurred while deleting the reminder 
                     from the database.
    """
    if reminder_get_from_database(reminder_id).get('id') is None:
        logger.error(f'Cannot deleting reminder {reminder_id}. Not found!')
        return False
    database_session.query(
        ReminderData
    ).filter(
        ReminderData.id == reminder_id
    ).delete()
    
    return try_to_commit(database_session)

def reminders_list_message(list_of_reminders: List[Dict[str, Union[str, int, datetime]]]) -> str:
    """Generates a message text for the user from of the list reminders.
    
    Return text message for the user of the list reminders.
    
    :param list_of_reminds: User Reminder List.
    :return: Return text message for the user of the list reminders.
    """
    text_message = '\n'.join(
        [settings.REMINDER_LIST_MESSAGE.format(remind.get('id'), remind.get('date_remind'),
            remind.get('comment'), remind.get('status')) for remind in list_of_reminders])
    
    return text_message


def month_remaining(reminder_date_month: str) -> int:
    """The function returns the number of month in the year at the time the 
       reminder was created.
    :param reminder_date: Date of reminder
    :return: The number of month remaining.
    """
    if datetime.now().year == int(reminder_date_month):
        return datetime.now().month
    else:
        return 1


def day_remaining(reminder_date_day: Dict[str, str]) -> Dict[str, int]:
    """The function returns the period of days in the reminder month.

    :param reminder_date: Date of reminder
    :return: The period of days for this month reminder.
    """ 
    days_period= {'start': 1,
                  'end': 31 }
    today_date = datetime.now()
    if int(reminder_date_day.get('month')) == int(
            today_date.month) and len(
                str(reminder_date_day.get('year'))) == 4:
        days_period['start'] = today_date.day
    
    try:
        year = int(reminder_date_day.get('year'))
        month = int(reminder_date_day.get('month'))
        start_month_day, days_period['end'] = calendar.monthrange(year, month)
    except ValueError as error:
        logger.error(error)
        return days_period

    return days_period
    

def hour_remaining(reminder_date_hour: str) -> int:
    """The function returns the number of hours in the date at the time the 
       reminder was created.
    :param reminder_date: Date of reminder
    :return: The number of hours remaining for this date.
    """
    today_date = datetime.now()
    try:
        convert_reminder_date = datetime.strptime(reminder_date_hour, '%d-%m-%Y')
        if today_date.replace(hour=0, minute=0, second=0, microsecond=0) == convert_reminder_date:
            return datetime.now().hour
        else:
            return 0
    except ValueError as error:
        logger.error(error)
        return 0


def minute_remaining(reminder_user_data: Dict[str, str], step: int) -> int:
    """The function returns the number of minutes 
       in the hour with a certain step.

    :param reminder_date: Date of reminder
    :return: The number of hours remaining for this date.
    """
    today_date = datetime.now()
    if 'day' in reminder_user_data:
        reminder_user_data['date'] = '{}-{}-{}'.format(
            reminder_user_data['day'], reminder_user_data['month'], reminder_user_data['year'])
    try:
        convert_reminder_date = datetime.strptime(
            reminder_user_data.get('date'), '%d-%m-%Y')
        if today_date.replace(
            minute=0, second=0, microsecond=0) == convert_reminder_date.replace(
                hour=int(reminder_user_data.get('hours', 0)), minute=0, second=0, microsecond=0):
                rate = (int(datetime.now().minute) // int(step)) + 1
                start_minute = rate * step
                return start_minute
        else:
            return 0
    except ValueError as error:
        logger.error(error)
        return 0

def userkey() -> str:
    """The function returns a key of 4 numbers.
    :return: Returns a four digit number
    """
    first = random.randint(0,9)
    second = random.randint(0,9)
    third = random.randint(0,9)
    fourth = random.randint(0,9)
    return f'{first}{second}{third}{fourth}'