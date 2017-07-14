"""Forms structure for Login and Editing user."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Login Form."""

    username = StringField("Name", validators=[DataRequired()])
    email = StringField("Email")
    password = StringField("Password", validators=[DataRequired()])


class EditForm(FlaskForm):
    """Edit user's profile Form."""

    username = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=200)])


class PostForm(FlaskForm):
    """Add a post as a user."""

    post = StringField('post', validators=[DataRequired()])
