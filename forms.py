#This file stores forms for the application.

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Search():
    query = StringField('query')
    search = SubmitField('Search')

class ComposeEmail(FlaskForm):
    to = StringField('to', validators=[DataRequired(),Email()])
    cc = StringField('cc')
    bcc = StringField('bcc')
    subject = StringField('Subject')
    body = TextAreaField('Body')
    submit = SubmitField('Send')

class ForwardEmail(FlaskForm):
    to = StringField('to', validators=[DataRequired(),Email()])
    cc = StringField('cc')
    bcc = StringField('bcc')
    subject = StringField('Subject')
    body = TextAreaField('Body')
    submit = SubmitField('Send')
