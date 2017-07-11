"""This file covers all test cases."""
# !flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User


class TestCase(unittest.TestCase):
    """Define a test case to be instantiated."""

    def setUp(self):
        """Set up."""
        app.config['TESTING'] = True  # testing environment
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Remove changes from the database in test."""
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        """Test avatar assignment."""
        u = User(username='john', email='john@example.com', password='112358')
        avatar = u.avatar(128)
        expected = ('http://www.gravatar.com/avatar/' +
                    'd4c74594d841139328695756648b6bd6')
        assert avatar[0:len(expected)] == expected
