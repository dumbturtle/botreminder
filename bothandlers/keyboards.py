from datetime import datetime, timedelta
from typing import List

from telegram import KeyboardButton, ReplyKeyboardMarkup

from settings import settings


def starting_keyboard() -> ReplyKeyboardMarkup:
    """The function forms the keyboard for the start page.

    :param: No
    :return: Reply Keyboard Markup
    """    
    starting_keyboard = ReplyKeyboardMarkup([['Хочу пользоваться!']], resize_keyboard=True)
    
    return starting_keyboard


def reminder_keyboard() -> ReplyKeyboardMarkup:
    """The function forms a keyboard for working with reminders.

    :param: No
    :return: Reply Keyboard Markup
    """ 
    work_keyboard = ReplyKeyboardMarkup([['Добавить напоминание', 'Список напоминаний', 'Удалить напоминание', 'Расхотел']], resize_keyboard=True)
    
    return work_keyboard


def reminder_add_date_keyboard() -> ReplyKeyboardMarkup:
    """The function forms a keyboard for selecting the 
       number of reminders. Three options are offered: 
       today, tomorrow, and enter the date in manual format.

    :param: No
    :return: Reply Keyboard Markup
    """ 
    today_date = datetime.today()
    today_date_keyboard = today_date.strftime("%d-%m-%Y")
    tomorrow_date_keyboard = (today_date + timedelta(days=1)).strftime("%d-%m-%Y")
    reminder_add_day_keyboard = ReplyKeyboardMarkup([[today_date_keyboard, tomorrow_date_keyboard, 'Ввести дату']], resize_keyboard=True)
    
    return reminder_add_day_keyboard


def reminder_add_digital_period_keyboard(start: int, end: int, keyboard_long: int, keyboard_step: int) -> ReplyKeyboardMarkup:
    """The function forms the keyboard based 
       on the parameters passed: start value, 
       finish value, keyboard length, and 
       step between values.

    :param start: Keyboard start value
    :param end: Keyboard Finish Value
    :param keyboard_long: Number of characters per line
    :param keyboard_step: Step between characters
    :return: Reply Keyboard Markup
    """ 
    end += 1
    key = []
    
    for keys in range(start, end, keyboard_long):
        keys_start = keys
        keys_end = keys + keyboard_long
        key.append([f'{key}' for key in range(keys_start, keys_end, keyboard_step) if key < end])
    digital_period_keyboard = ReplyKeyboardMarkup(key, resize_keyboard=True)
    
    return digital_period_keyboard


def remind_list_for_delete_keyboard(reminder_list: List[str]) -> ReplyKeyboardMarkup:
    """The function forms the keyboard on the basis 
       of the transmitted sheet with a list of reminder ID.

    :param reminder_list: List of Reminder ID
    :return: Reply Keyboard Markup
    """ 
    keyboard = ReplyKeyboardMarkup([reminder_list], resize_keyboard=True)
    
    return keyboard


def remind_confirm_for_delete_keyboard() -> ReplyKeyboardMarkup:
    """The function forms a keyboard with the offer 
       to select Yes / No to confirm or cancel the 
       deletion of the reminder..

    :param: No
    :return: Reply Keyboard Markup
    """ 
    delete_keyboard = ReplyKeyboardMarkup([['Да', 'Нет']], resize_keyboard=True)
    
    return delete_keyboard
