from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode, error, InlineKeyboardMarkup, InlineKeyboardButton	
from telegram.ext import ConversationHandler
from telegram.ext import messagequeue as mq 

import settings, logging, os


from utils import *
from db import *


def greet_user(bot, update, user_data):
	message_text = settings.JOIN_TEXT
	update.message.reply_text(message_text, reply_markup=get_keyboard())

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
		text_message = f'{commit_status}, уже есть!'
	
	update.message.reply_text(text_message, reply_markup=get_keyboard())

def unjoin_user(bot, update, user_data):
	commit_status = delete_user_from_database(database_session, update.effective_user.id)
	
	if commit_status == 'Commited':
		text_message = "Вас больше нет в базе!"
	elif commit_status == 'Error':
		text_message = "Ошибка:("
	else:
		text_message = "Нет такого пользователя:("
	
	update.message.reply_text(text_message, reply_markup=get_keyboard())