"""This file covers all test cases."""
# !flask/bin/python
import os
import unittest
from datetime import datetime, timedelta as td

from config import basedir
from app import app, db
from app.models import User, Post

# Test users
test_username = 'test'
test_username_1 = 'test1'
test_username_2 = 'test2'
test_username_3 = 'test3'
test_username_4 = 'test4'


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
        u = User(username=test_username_1,
                 email='a@example.com',
                 password='secret')
        v = User(username=test_username_2,
                 email='b@example.com',
                 password='secret')
        db.session.add(u)
        db.session.add(v)
        db.session.commit()
        u.follow(u)
        v.follow(v)
        db.session.add(u)
        db.session.add(v)
        db.session.commit()
        self.assertIsNone(u.unfollow(v),
                          msg='User is defaulted as following all other users')
        self.assertIsNone(u.unfollow(u),
                          msg='User is allowed to unfollow himself')
        # U follows V
        u = u.follow(v)
        db.session.add(u)
        db.session.commit()
        self.assertIsNone(u.follow(v),
                          msg='Follow test failed.')
        self.assertTrue(u.is_following(v),
                          msg='Follow test failed.')
        self.assertTrue(u.followed.count() == 2,  # himself and V
                          msg='Follow test failed.')
        self.assertTrue(u.followed.first().username == u.username,
                          msg='Follow test failed.')
        # Create test for confirming U follows V.
        # TO DO
        self.assertTrue(v.followers.count() == 2,
                          msg='Follow test failed.')
        self.assertTrue(v.followers.first().username == v.username,
                          msg='Follow test failed.')
        # Create test for confirming V follows U.
        # TO DO

        # U unfollows V
        u = u.unfollow(v)
        self.assertIsNotNone(u,
                             msg='Unfollow test failed.')
        db.session.add(u)
        db.session.commit()
        self.assertFalse(u.is_following(v),
                             msg='Unfollow test failed.')
        self.assertTrue(u.followed.count() == 1,
                             msg='Unfollow test failed.')
        self.assertTrue(v.followers.count() == 1,
                             msg='Unfollow test failed.')

    def test_follow_posts(self):
        """Test creation, visualization and deletion of posts."""
        # Create users
        u1 = User(username=test_username_1, email='a@sample.com', password='1')
        u2 = User(username=test_username_2, email='b@sample.com', password='2')
        u3 = User(username=test_username_3, email='c@sample.com', password='3')
        u4 = User(username=test_username_4, email='d@sample.com', password='4')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        # Create posts
        utcnow = datetime.utcnow()
        p1 = Post(body='post 1', author=u1, timestamp=utcnow + td(seconds=1))
        p2 = Post(body='post 2', author=u2, timestamp=utcnow + td(seconds=2))
        p3 = Post(body='post 3', author=u3, timestamp=utcnow + td(seconds=3))
        p4 = Post(body='post 4', author=u4, timestamp=utcnow + td(seconds=4))
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.commit()
        # People is following people.
        u1.follow(u1)
        u1.follow(u2)
        u1.follow(u4)  # u1 follows himself, u2, u4. u1 does not follow u3.
        u2.follow(u2)
        u2.follow(u3)  # u2 follows himself, u3. u2 does not follow u1, u4.
        u3.follow(u3)
        u3.follow(u4)  # u3 follows himself, u4. u3 does not follow u1, u2.
        u4.follow(u4)  # u4 follows himself.     u4 does not follow anyone else
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()

        # Check the followed posts of each user.
        f1 = u1.get_followed_posts().all()
        f2 = u2.get_followed_posts().all()
        f3 = u3.get_followed_posts().all()
        f4 = u4.get_followed_posts().all()
        # Assert that the number of folwd posts is correct (1 per folwd. user)
        self.assertEqual(len(f1), 3, msg='Follow F')  # u1 follows u1,u2,  ,u4
        self.assertEqual(len(f2), 2, msg='Follow F')  # u2 follows   ,u2,u3,
        self.assertEqual(len(f3), 2, msg='Follow F')  # u3 follows   ,  ,u3,u4
        self.assertEqual(len(f4), 1, msg='Follow F')  # u4 follows   ,  ,  ,u4
        self.assertEqual(f1, [p4, p2, p1], msg='Posts followed failed')
        self.assertEqual(f2, [p3, p2], msg='Posts followed failed')
        self.assertEqual(f3, [p4, p3], msg='Posts followed failed')
        self.assertEqual(f4, [p4], msg='Posts followed failed')


if __name__ == '__main__':
    unittest.main()
