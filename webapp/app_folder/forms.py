from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UserIdForm(FlaskForm):
    userid = StringField('UserID', validators = [DataRequired()])
    submit = SubmitField('Ok')

class UserKeyForm(FlaskForm):
    userkey = StringField('UserKey', validators = [DataRequired()])
    submit = SubmitField('Ok')

