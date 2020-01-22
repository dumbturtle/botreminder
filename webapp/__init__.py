
from flask import Flask
from flask_login import LoginManager
from settings import connect_settings

app = Flask(__name__)
app.config['SECRET_KEY'] = connect_settings.WEB_APP
login = LoginManager(app)


from webapp.app_folder import routes
