from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from wtforms_validators import Integer 


class UserIdForm(FlaskForm):
    """The class that forms the form for the user identifier input page.

    """
    userid = StringField('UserID', validators=[DataRequired(), Integer(message='Only numeric')])
    submit = SubmitField('Ok')


class UserKeyForm(FlaskForm):
    """The class forming the form for the key entry page that the user receives.
    """
    userkey = StringField('UserKey', validators=[DataRequired(), Integer(message='Only numeric')])
    submit = SubmitField('Ok')
