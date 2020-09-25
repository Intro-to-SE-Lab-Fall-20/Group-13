#This file stores forms for the application.

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Search():
    query = StringField('query')
    submit = SubmitField('Search')

class ComposeEmail(FlaskForm):
    to = StringField('email', validators=[DataRequired(),Email()])
    cc = StringField('email', validators=[DataRequired(),Email()])
    bcc = StringField('email', validators=[DataRequired(),Email()])
    subject = StringField()
    body = StringField()
    submit = SubmitField('Send')
