from flask import render_template, url_for

from database.modeldb import ReminderData, database_session
from app import app


@app.route('/')
@app.route('/reminder')
def reminder():
    reminder_list = database_session.query(
        ReminderData
    ).filter(
        ReminderData.status == 'active'
    ).all()
    return render_template(url_for('reminder'), title='Home', reminder_list=reminder_list)
