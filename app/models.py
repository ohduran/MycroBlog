"""
Database structure.
It is always best to move the logic of our application away from view functions
and into models, because that simplifies the testing.
"""
from hashlib import md5
from app import db

# Auxiliary table that connects followers with followed users.
# Both key point to users table.
followers = db.Table('followers',
                     db.Column('follower_id',
                                db.Integer,
                                db.ForeignKey('user.id')),
                     db.Column('followed_id',
                                db.Integer,
                                db.ForeignKey('user.id')))


class User(db.Model):
    """User structure in database."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    password = db.Column(db.String(10))
    # define follow relationship
    # Link User instances with other User instances.
    # Convention: For a pair of users, left side is follower, right is followed
    # When quering from the left, we will get the followed users.
    followed = db.relationship('User',  # right side entity
                               secondary=followers,  # association table
                               # Condition that links left side to association
                               primaryjoin=(followers.c.follower_id == id),
                               # Condition that links right side to association
                               secondaryjoin=(followers.c.followed_id == id),
                               # How this will be accessed from right side
                               backref=db.backref('followers', lazy='dynamic'),
                               # Lazy means 'Not run until specified'
                               lazy='dynamic')

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

    @staticmethod
    def make_unique_username(username):
        """Avoid repetition of username in database by adding '2' to it."""
        if User.query.filter_by(username=username).first() is None:
            return username
        version = 2
        while True:
            new_username = username + str(version)
            if User.query.filter_by(username=new_username).first() is None:
                break
            version += 1
        return new_username

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

    # Add and remove Follower relationships.
    def is_following(self, user):
        """Is self following user."""
        # Check if the associated table includes a self -> user row.
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        """Make self follow user."""
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        """Make self unfollow user. User cannot unfollow himself."""
        if self.is_following(user) and user is not self:
            self.followed.remove(user)
            return self

    # Relational databases work really well with querying posts
    # for followed users.
    def get_followed_posts(self):
        """Get followed posts."""
        return Post.query.join(  # join will concatenate Post with :
            followers,  # associated followers table
            # condition: followed id is the user id
            (followers.c.followed_id == Post.user_id)).filter(
                # On that temporary table, filter user_id = self.id
                followers.c.follower_id == self.id).order_by(
                    # order by timestamp in descending order (latest first)
                    Post.timestamp.desc())

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
