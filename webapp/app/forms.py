from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UserIdForm(FlaskForm):
    """The class that forms the form for the user identifier input page.

    """
    userid = StringField('UserID', validators=[DataRequired()])
    submit = SubmitField('Ok')


class UserKeyForm(FlaskForm):
    """The class forming the form for the key entry page that the user receives.
    """
    userkey = StringField('UserKey', validators=[DataRequired()])
    submit = SubmitField('Ok')
