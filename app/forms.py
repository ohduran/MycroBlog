"""Forms structure for Login, Registering and Editing."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("Name", validators=[DataRequired()])
    email = StringField("Email")
    password = StringField("Password", validators=[DataRequired()])


class EditForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=200)])
