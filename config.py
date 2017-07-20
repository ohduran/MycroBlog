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


# administrator list

ADMINS = ['mycroblogduran@gmail.com']

# Pagination
POSTS_PER_PAGE = 3
