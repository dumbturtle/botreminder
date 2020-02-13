from flask import Flask
from flask_login import LoginManager

from database.modeldb import User, database_session
from settings import connect_settings

login = LoginManager()
login.login_view = 'login'

def creat_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = connect_settings.WEB_APP
    
    login.init_app(app)

    with app.app_context():
        from webapp.app import routes

    return app


@login.user_loader
def load_user(user_id):
    """Function request data by user ID.

    :return: user information
    """
    return database_session.query(User).filter(User.id == user_id).first()