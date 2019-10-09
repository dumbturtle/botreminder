from telegram import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta

import settings



def starting_keyboard():
	#join_button = KeyboardButton('Прислать контакты', request_contact=True)
	#location_button = KeyboardButton('Прислать координаты', request_location=True)
	starting_keyboard = ReplyKeyboardMarkup([['Хочу пользоваться!', 'Добавить напоминание', 
										'Расхотел']], resize_keyboard=True)
	return starting_keyboard   	  

def reminder_keyboard():
	work_keyboard = ReplyKeyboardMarkup([['Добавить напоминание', 'Список напоминаний',
										'Удалить напоминание']], resize_keyboard=True)
	return work_keyboard

def reminder_add_day_keyboard():
	today_date = datetime.today()
	today_date_keyboard = today_date.strftime("%d-%m-%Y")
	tomorrow_date_keyboard = (today_date + timedelta(days=1)).strftime("%d-%m-%Y")
	reminder_add_day_keyboard = ReplyKeyboardMarkup([[today_date_keyboard, tomorrow_date_keyboard,
										'Ввести дату']], resize_keyboard=True)
	return reminder_add_day_keyboard

def reminder_add_digital_period_keyboard(period):
	if period == 'day':
		key = [[str(x) for x in range(1,12)],
			   [str(x) for x in range(12,24)],
			   [str(x) for x in range(24,32)]]
	elif period == 'month':
		key = [[str(x) for x in range(1,13)]]
	elif period == 'year':
		key = [[str(x) for x in range(2019,2024)]]
	digital_period_keyboard = ReplyKeyboardMarkup(key, resize_keyboard=False)
	return digital_period_keyboard

