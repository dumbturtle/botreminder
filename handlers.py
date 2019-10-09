from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode, error, InlineKeyboardMarkup, InlineKeyboardButton	
#from telegram.ext import ConversationHandler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler
from telegram.ext import messagequeue as mq 

import settings, logging, os


from keyboards import *
from db import *


def greet_user(bot, update, user_data):
	commit_status = check_user_in_database(database_session, update.effective_user.id)
	if commit_status == "No user":
		message_text = settings.JOIN_TEXT
		update.message.reply_text(message_text, reply_markup=starting_keyboard())
	else:
		message_text = settings.JOIN_TEXT_FOR_USER.format(commit_status)
		update.message.reply_text(message_text, reply_markup=reminder_keyboard())

def join_user(bot, update, user_data):
	commit_status  = add_user_to_database(database_session, update.effective_user.id, 
			update.effective_user.first_name,
			update.effective_user.last_name,
			update.effective_user.username,
			update.message.chat_id)
	
	if commit_status == 'Commited':
		text_message = "Вы в базе!"
	elif commit_status == 'Error':
		text_message = "Ошибка:("
	else:
		commit_status = commit_status[0].first_name
		text_message = f'{commit_status}, уже есть!'
	
	update.message.reply_text(text_message, reply_markup=reminder_keyboard())

def unjoin_user(bot, update, user_data):
	commit_status = delete_user_from_database(database_session, update.effective_user.id)
	
	if commit_status == 'Commited':
		text_message = "Вас больше нет в базе!"
	elif commit_status == 'Error':
		text_message = "Ошибка:("
	else:
		text_message = "Нет такого пользователя:("
	
	update.message.reply_text(text_message, reply_markup=starting_keyboard())

def check_user(bot, update, user_data):
	commit_status = check_user_in_database(database_session, update.effective_user.id)
	
	if commit_status == 'No user':
		text_message = "Пока вы не пользуетесь ботом:("
	else:
		commit_status = commit_status[0].first_name
		text_message = f'{commit_status}, вы в нашей базе!'
	
	update.message.reply_text(text_message, reply_markup=starting_keyboard())

def reminder_add(bot, update, user_data):
	text_message = 'Введите дату напоминания!'
	update.message.reply_text(text_message, reply_markup=reminder_add_day_keyboard())
	return "reminder_add_date"

def reminder_add_date(bot, update, user_data):
	user_data['date'] = update.message.text
	text_message = 'Введите комментарий!'
	update.message.reply_text(text_message , reply_markup=ReplyKeyboardRemove())
	return "reminder_add_comment"

def reminder_add_comment(bot, update, user_data):
	text_message = 'Записываю'
	user_data['comment'] = update.message.text
	update.message.reply_text(text_message, reply_markup=ReplyKeyboardRemove())
	print(user_data)
	return ConversationHandler.END

def reminder_skip_comment(bot, update, user_data):
	text_message = 'Записываю'
	user_data['comment'] = 'Нет комментария!'
	update.message.reply_text(text_message, reply_markup=ReplyKeyboardRemove())
	print(user_data)
	return ConversationHandler.END

def calendar_add_date(bot, update, user_data):
	text_message = 'Введите число!'
	update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard('day'))
	return "calendar_add_day"

def calendar_add_day(bot, update, user_data):
	text_message = 'Введите месяц в числовом формате!'
	user_data['day'] = update.message.text
	update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard('month'))
	return "calendar_add_month"

def calendar_add_month(bot, update, user_data):
	text_message = 'Введите год!'
	user_data['month'] = update.message.text
	update.message.reply_text(text_message, reply_markup=reminder_add_digital_period_keyboard('year'))
	return "calendar_add_year"

def calendar_add_year(bot, update, user_data):
	user_data['year'] = update.message.text
	user_data['date'] = f'{user_data["day"]}-{user_data["month"]}-{user_data["year"]}'
	print(user_data)
	text_message = 'Введите комментарий!'
	update.message.reply_text(text_message, reply_markup=ReplyKeyboardRemove())
	return "reminder_add_comment"
  


def dontknow(bot, update, user_data):
	update.message.reply_text("Не понимаю!", reply_markup=reminder_keyboard())
