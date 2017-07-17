"""Config file."""
# CRSF configuration
WTF_CSRF_ENABLED = False
SECRET_KEY = 'very-hard-to-guess-key'

# Database configuration in SQLAlchemy
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Mail server settings

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TSL = False
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = 'mycroblogduran@gmail.com'
MAIL_USERNAME = os.environ.get('mycroblogduran@gmail.com')
MAIL_PASSWORD = os.environ.get('09111991')

# administrator list

ADMINS = ['mycroblogduran@gmail.com']

# Pagination
POSTS_PER_PAGE = 3

# Text search in WhooshAlchemy
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50
