from flask import Flask
from settings import connect_settings

app = Flask(__name__)
app.config['SECRET_KEY'] = connect_settings.WEB_APP

from webapp.app_folder import routes