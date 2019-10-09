from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler
from telegram.ext import messagequeue as mq


import logging
import settings

from keyboards import *
from handlers import *

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')


def main():
	mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
	#mybot = Updater(settings.API_KEY)
	#mybot.bot._msg_queue = mq.MessageQueue()
	#mybot.bot._is_messages_queued_default = True

	logging.info('Бот запускается')


	dp = mybot.dispatcher
	

	#mybot.job_queue.run_repeating(send_updates, interval=5)
	
	reminder_create = ConversationHandler(
		entry_points=[RegexHandler('^(Добавить напоминание)$', reminder_add, pass_user_data=True)],
		states={
			"reminder_add_date": [RegexHandler('^(Ввести дату)$', calendar_add_date, pass_user_data=True),
								  MessageHandler(Filters.text, reminder_add_date, pass_user_data=True)],
			"calendar_add_day": [RegexHandler('^([1-9]|0[0-9]|1[0-9]|2[0-9]|3[0-1])$', calendar_add_day, pass_user_data=True)],
			"calendar_add_month": [RegexHandler('^([1-9]|0[0-9]|1[0-2])$', calendar_add_month, pass_user_data=True)],
			"calendar_add_year": [RegexHandler('^([0-9][0-9][0-9][0-9])$', calendar_add_year, pass_user_data=True)],
			"reminder_add_comment": [MessageHandler(Filters.text, reminder_add_comment, pass_user_data=True),
								  CommandHandler('skip', reminder_skip_comment, pass_user_data=True)]
			},
		fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document, 
			dontknow, 
			pass_user_data=True
			)]
	)
	
	dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
	dp.add_handler(RegexHandler('^(Хочу пользоваться!)$', join_user, pass_user_data=True))
	dp.add_handler(RegexHandler('^(Расхотел)$', unjoin_user, pass_user_data=True))
	dp.add_handler(RegexHandler('^(Проверка регистрации)$', check_user, pass_user_data=True))
	dp.add_handler(reminder_create)
	dp.add_handler(MessageHandler(Filters.text, dontknow, pass_user_data=True))
	'''
	dp.add_handler(CallbackQueryHandler(inline_button_pressed))
	dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
	dp.add_handler(CommandHandler("sub",subscribe))  
	dp.add_handler(CommandHandler("unsub",unsubscribe))
	dp.add_handler(CommandHandler("alarm",set_alarm, pass_args=True, pass_job_queue=True))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
	'''
	mybot.start_polling()
	mybot.idle()


if __name__ == "__main__":
	main()
