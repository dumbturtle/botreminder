from telegram import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta

import settings



def starting_keyboard():
	#join_button = KeyboardButton('Прислать контакты', request_contact=True)
	#location_button = KeyboardButton('Прислать координаты', request_location=True)
	starting_keyboard = ReplyKeyboardMarkup([['Хочу пользоваться!', 'Расхотел']], resize_keyboard=True)
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

def reminder_add_digital_period_keyboard_a(period):
	if period == 'day':
		key = [[str(x) for x in range(1,11)],
			   [str(x) for x in range(11,22)],
			   [str(x) for x in range(22,32)]]
	elif period == 'month':
		key = [[str(x) for x in range(1,7)],
				[str(x) for x in range(7,13)]]
	elif period == 'year':
		key = [[str(x) for x in range(2019,2024)]]
	elif period == 'hours':
		key = [[str(x) for x in range(0,9)	],
			   [str(x) for x in range(9,18)	],
			   [str(x) for x in range(18,24)]]
	elif period == 'minutes':
		key = [[str(x) for x in range(0,60,15)]]

	digital_period_keyboard = ReplyKeyboardMarkup(key, resize_keyboard=False)
	return digital_period_keyboard

def reminder_add_digital_period_keyboard(start, end, keyboard_long, keyboard_step):
	end += 1
	key = []
	for keys in range(start, end, keyboard_long):
  		key.append([ f'{key}' for key in range(keys, keys + keyboard_long, keyboard_step)  if key < end])
	#return key
	digital_period_keyboard = ReplyKeyboardMarkup(key, resize_keyboard=False)
	return digital_period_keyboard


if __name__ == "__main__":
	print(reminder_add_digital_period_keyboard(0,59,10,15))