from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler
from telegram.ext import messagequeue as mq


import logging
import settings

from utils import *
from handlers import *

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')


def main():
	mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
	#mybot.bot._msg_queue = mq.MessageQueue()
	#mybot.bot._is_messages_queued_default = True

	logging.info('Бот запускается')


	dp = mybot.dispatcher
	

	#mybot.job_queue.run_repeating(send_updates, interval=5)
	'''
	anketa = ConversationHandler(
		entry_points=[RegexHandler('^(Заполнить анкету)$', anketa_start, pass_user_data=True)],
		states={
			"name": [MessageHandler(Filters.text, anketa_get_name, pass_user_data=True)],
			"rating": [RegexHandler('^(1|2|3|4|5)$', anketa_rating, pass_user_data=True)],  
			"comment": [MessageHandler(Filters.text, anketa_comment, pass_user_data=True),
						CommandHandler('skip', anketa_skip_comment, pass_user_data=True)]
			},
		fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document, 
			dontknow, 
			pass_user_data=True
			)]
	)
	'''
	dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
	dp.add_handler(RegexHandler('^(Хочу пользоваться!)$', join_user, pass_user_data=True))
	dp.add_handler(RegexHandler('^(Расхотел)$', unjoin_user, pass_user_data=True))
	#dp.add_handler(CommandHandler('^(Пользуюсь ли я?)$', check_user, pass_user_data=True))
	
	'''
	dp.add_handler(anketa)
	dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
	dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
	dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
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
