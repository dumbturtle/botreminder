from telegram import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta

import settings



def starting_keyboard():
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

def reminder_add_digital_period_keyboard(start, end, keyboard_long, keyboard_step):
	end += 1
	key = []
	for keys in range(start, end, keyboard_long):
  		key.append([ f'{key}' for key in range(keys, keys + keyboard_long, keyboard_step)  if key < end])
	
	digital_period_keyboard = ReplyKeyboardMarkup(key, resize_keyboard=True)
	return digital_period_keyboard

def remind_list_for_delete_keyboard(remind_list):
	keyboard = ReplyKeyboardMarkup([remind_list], resize_keyboard=True)
	return keyboard

def remind_confirm_for_delete_keyboard():
	delete_keyboard = ReplyKeyboardMarkup([['Да', 'Нет']], resize_keyboard=True)
	
	return delete_keyboard

if __name__ == "__main__":
	pass