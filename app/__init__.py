"""Init file."""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import basedir


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail()
mail.init_app(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'  # for Flask to know what view logs users in.

from app import views, models
