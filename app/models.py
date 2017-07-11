"""Database structure."""
from hashlib import md5
from app import db


class User(db.Model):
    """User structure in database."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    password = db.Column(db.String(10))

    @property
    def is_authenticated(self):
        """Flask requirement for authentication and security."""
        return True

    @property
    def is_active(self):
        """Flask requirement for authentication and security."""
        return True

    @property
    def is_anonymous(self):
        """Flask requirement for authentication and security."""
        return False

    def get_id(self):
        """Get id of the user for database purposes."""
        return unicode(self.id)

    def avatar(self, size):
        """Avatar for representation purposes."""
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % \
            (md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        """Return username."""
        return '<User %r>' % (self.username)

# Implement OAuth protocol following
# https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask


class Post(db.Model):
    """Post database structure."""

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """Print post."""
        return '<Post %r>' % (self.body)
