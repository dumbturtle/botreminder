from flask import Flask
from flask_login import LoginManager

from database.modeldb import User, database_session
from settings import connect_settings


app = Flask(__name__)
app.config['SECRET_KEY'] = connect_settings.WEB_APP
app.config['DEBUG'] = True
login = LoginManager(app)
login.login_view = 'login'


@login.user_loader
def load_user(user_id):
    """Function request data by user ID.
    :return: user information
    """
    return database_session.query(User).filter(User.id == user_id).first()


from webapp.app_folder import routes