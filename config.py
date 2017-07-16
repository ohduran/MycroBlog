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

MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list

ADMINS = ['alvaro.duranb@gmail.com']

# Pagination
POSTS_PER_PAGE = 3

# Text search in WhooshAlchemy
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50
