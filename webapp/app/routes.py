from datetime import datetime

from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from bothandlers.utils import (get_information_about_user,
                               reminder_list_from_database,
                               reminders_list_message, user_key)
from database.modeldb import ReminderData, User, database_session
from reminderhandlers.reminds_handlers import send_notification_reminder
from webapp import login
from webapp.app.forms import UserIdForm, UserKeyForm

# Global variables
USER_KEY_FROM_MESSAGE = int


@app.route('/')
@app.route('/index')
def index():
    """Page processing function "/index"
        
    If the user has registered on the site, he is redirected to the page with a reminder.
    If the user is not registered, a blank page is displayed.
    """

    if current_user.is_authenticated:
        telegram_user_id = database_session.query(User.telegram_user_id).filter(
            User.id == current_user.get_id()).first()
        return redirect(url_for('reminder', userid=telegram_user_id))
    return render_template('index.html', title='Main')


@app.route('/login', methods=['GET', 'POST'])
def login() -> render_template:
    """Page processing function "/login"
    
    If the user is registered, he is immediately redirected to the page with reminders.
    When you click on the "OK" button, it checks if the user is in the database, 
    if there is no user, an error is displayed. If the user is in the system, 
    a PIN code is generated and sent to the user in the Telegram. 
    Redirected to the key entry page.
    """
    form = UserIdForm()

    if current_user.is_authenticated:
        telegram_user_id = database_session.query(User.telegram_user_id).filter(
            User.id == current_user.get_id()).first()
        return redirect(url_for('reminder', userid=telegram_user_id))

    if form.validate_on_submit():
        user = database_session.query(User).filter(
            User.telegram_user_id == form.userid.data).first()
        if user is None:
            flash("No Id")
            return redirect(url_for('login'))
        USER_KEY_FROM_MESSAGE = user_key()
        user_text = f'Выш код для входа: {USER_KEY_FROM_MESSAGE}'
        send_notification_reminder(
            user.telegram_user_id, datetime.now(), user_text)
        return redirect(url_for('loginkey', userid=user.telegram_user_id))
    return render_template('login.html', title='Login In', form=form)


@app.route('/logout')
def logout() -> redirect:
    """Page processing function "/logout"
    
    User Logout Function
    """
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    logout_user()
    return redirect(url_for('index'))


@app.route('/loginkey', methods=['GET', 'POST'])
def loginkey():
    """Page processing function "/loginkey"
    
    When you click "OK", the function 
    checks the entered PIN code. If the 
    PIN code is correct, then the user logs 
    in and is redirected to the reminder page. 
    If the pin code is wrong, an error message is displayed.
    """
    keyform = UserKeyForm()

    if current_user.is_authenticated:
        telegram_user_id = database_session.query(User.telegram_user_id).filter(
            User.id == current_user.get_id()).first()
        return redirect(url_for('reminder', userid=telegram_user_id))
    
    user_id = request.args.get('userid', None)

    if user_id is None:
        flash('No UserId')
        return redirect(url_for('login'))
    
    user = database_session.query(User).filter(
        User.telegram_user_id == user_id).first()
    if keyform.validate_on_submit():
        keyform.userkey.data == str(USER_KEY_FROM_MESSAGE)
        login_user(user)
        return redirect(url_for('reminder', userid=user_id))
    flash('Error PIN Code')
    return render_template('loginkey.html', title='Key In', form=keyform)


@app.route('/reminder')
@login_required
def reminder():
    """Page processing function "/reminder"
    
    The function, based on the user ID, requests 
    reminders from the data.
    """
    userid = request.args.get('userid', None)

    if userid is None:
        userid = database_session.query(User.telegram_user_id).filter(
            User.id == current_user.get_id()).first()
    user_info = get_information_about_user(userid)
    list_reminders = reminder_list_from_database(userid)
    return render_template('reminder.html', title='List Reminder', reminder_list=list_reminders, user_info=user_info)
    
