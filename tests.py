"""This file covers all test cases."""
# !flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User

# Test users
test_username = 'test1'
test_username_2 = 'test2'


class BaseTest(unittest.TestCase):
    """Define a test case to be instantiated."""

    def setUp(self):
        """Set up."""
        app.config['TESTING'] = True  # testing environment
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Remove changes from the database in test."""
        db.session.remove()
        db.drop_all()

    def test_user_exists_in_database_when_added(self):
        """Test that the user being added exists in the database."""
        u = User(username=test_username,
                 email='a@example.com',
                 password='secret')
        db.session.add(u)
        db.session.commit()
        username_used = User.query.filter_by(
            username=u.username).first()
        # msg will display Error message.
        self.assertEqual(username_used, u,
                         msg='User is not added to DB.')

    def test_duplicates_change_name_with_version(self):
        """
        Adding duplicate usernames.
        When adding a duplicate name in database,
        username is changed into username+str(version).
        """
        # Add username in database
        u = User(username=test_username,
                 email='a@example.com',
                 password='secret')
        db.session.add(u)
        db.session.commit()
        # Create the same username again.
        again_username = User.make_unique_username(test_username)
        # New username doesn't match with the old one.
        self.assertNotEqual(again_username, test_username,
                            msg='Unique names in db failed')

    def test_follow(self):
        """Test user following and unfollowing another existing user."""
        # Create users in database.
        u = User(username=test_username,
                 email='a@example.com',
                 password='secret')
        v = User(username=test_username_2,
                 email='b@example.com',
                 password='secret')
        db.session.add(u)
        db.session.add(v)
        db.session.commit()
        self.assertIsNone(u.unfollow(v),
                          msg='User is defaulted as following all other users')
        # U follows V
        u = u.follow(v)
        db.session.add(u)
        db.session.commit()
        self.assertIsNone(u.follow(v),
                          msg='Follow test failed.')
        self.assertTrue(u.is_following(v),
                          msg='Follow test failed.')
        self.assertTrue(u.followed.count() == 1,
                          msg='Follow test failed.')
        self.assertTrue(u.followed.first().username == test_username_2,
                          msg='Follow test failed.')
        self.assertTrue(v.followers.count() == 1,
                          msg='Follow test failed.')
        self.assertTrue(v.followers.first().username == test_username,
                          msg='Follow test failed.')
        # U unfollows V
        u = u.unfollow(v)
        self.assertIsNotNone(u,
                             msg='Unfollow test failed.')
        db.session.add(u)
        db.session.commit()
        self.assertFalse(u.is_following(v),
                             msg='Unfollow test failed.')
        self.assertTrue(u.followed.count() == 0,
                             msg='Unfollow test failed.')
        self.assertTrue(v.followers.count() == 0,
                             msg='Unfollow test failed.')


if __name__ == '__main__':
    unittest.main()
