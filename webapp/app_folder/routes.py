from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_user

from bothandlers.utils import get_information_about_user, reminder_list_from_database, reminders_list_message
from database.modeldb import ReminderData, database_session, User

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


@app.route('/login', methods= ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('reminder'))
    form = UserIdForm()
    if form.validate_on_submit():
        user = User.query.filter_by(telegramm_user_id=form.userid.data).first()
        if user is None:
            flash('Нет такого пользователя')
        return redirect(url_for('reminder'))
    return render_template('login.html', title='Login In', form=form)
