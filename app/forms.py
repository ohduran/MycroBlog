from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    username = StringField("Name", validators=[DataRequired()])
    email = StringField("Email")
    password = StringField("Password", validators=[DataRequired()])


class EditForm(Form):
    username = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=200)])
