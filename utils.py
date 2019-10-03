from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings


def get_keyboard():
	#join_button = KeyboardButton('Прислать контакты', request_contact=True)
	#location_button = KeyboardButton('Прислать координаты', request_location=True)
	my_keyboard = ReplyKeyboardMarkup([['Хочу пользоваться!', 'Расхотел', 
										'Пользуюсь ли я?']], resize_keyboard=True)
	return my_keyboard   	  
	  
#if __name__ == "__main__":
