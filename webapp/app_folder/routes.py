from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from bothandlers.utils import (get_information_about_user,
                               reminder_list_from_database,
                               reminders_list_message, userkey)
from database.modeldb import ReminderData, User, database_session
from reminderhandlers.reminds_handlers import sending_notification_reminder
from webapp import app
from webapp.app_folder.forms import UserIdForm, UserKeyForm

# Global variables
key = 0


@app.route('/')
@app.route('/index')
def index():
    """Page processing function "/index"
        If the user has registered on the site, he is redirected to the page with a reminder.
        If the user is not registered, a blank page is displayed.
    """
    if current_user.is_authenticated:
        telegramm_user_id = database_session.query(User.telegramm_user_id).filter(
            User.id == current_user.get_id()).first()
        return redirect(url_for('reminder', userid=telegramm_user_id))
    return render_template('index.html', title='Main')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page processing function "/login"
        If the user is registered, he is immediately redirected to the page with reminders.
        When you click on the "OK" button, it checks if the user is in the database, 
        if there is no user, an error is displayed. If the user is in the system, 
        a PIN code is generated and sent to the user in the Telegram. 
        Redirected to the key entry page.
    """
    form = UserIdForm()
    user = database_session.query(User).filter(
        User.telegramm_user_id == form.userid.data).first()
    if current_user.is_authenticated:
        return redirect(url_for('reminder', userid=user.telegramm_user_id))
    if form.validate_on_submit():
        if user is None:
            flash('No user')
            return redirect(url_for('login'))
        key = userkey()
        usertext = f'Выш код для входа: {key}'
        sending_notification_reminder(
            user.telegramm_user_id, datetime.now(), usertext)
        return redirect(url_for('loginkey', userid=user.telegramm_user_id))
    return render_template('login.html', title='Login In', form=form)


@app.route('/logout')
def logout():
    """Page processing function "/logout"
        User Logout Function
    """
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
    userid = request.args.get('userid', None)
    user = database_session.query(User).filter(
        User.telegramm_user_id == userid).first()
    if keyform.validate_on_submit():
        keyform.userkey.data == str(key)
        login_user(user)
        return redirect(url_for('reminder', userid=userid))
    flash('Error PIN Code')
    return render_template('loginkey.html', title='Key In', form=keyform)


@app.route('/reminder')
@login_required
def reminder():
    """Page processing function "/reminder"
        The function, based on the user ID, requests 
        reminders from the data.
    """
    if current_user.is_authenticated:
        userid = request.args.get('userid', None)
        user_info = get_information_about_user(userid)
        list_reminders = reminder_list_from_database(userid)
        return render_template('reminder.html', title='List Reminder', reminder_list=list_reminders, user_info=user_info)
    return redirect(url_for('index'))
