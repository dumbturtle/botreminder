from flask import render_template, url_for

from bothandlers.utils import get_information_about_user, reminder_list_from_database, reminders_list_message
from database.modeldb import ReminderData, database_session

from webapp import app
from webapp.app_folder.forms import UserIdForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Main')


@app.route('/reminder')
def reminder():
    user_id = 714084509
    user_info = get_information_about_user(user_id)
    list_reminders = reminder_list_from_database(user_id)
 
    return render_template('reminder.html', title='List Reminder', reminder_list=list_reminders, user_info = user_info)


@app.route('/login')
def login():
    form = UserIdForm()
    return render_template('login.html', title='Login In', form=form)
