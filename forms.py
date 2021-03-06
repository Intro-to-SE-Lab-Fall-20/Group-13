#This file stores forms for the application.

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField,TextAreaField, FileField
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
    fileName = FileField('File')
    submit = SubmitField('Send')

class ForwardEmail(FlaskForm):
    to = StringField('to', validators=[DataRequired(),Email()])
    cc = StringField('cc')
    bcc = StringField('bcc')
    subject = StringField('Subject')
    body = TextAreaField('Body')
    file = FileField('file')
    submit = SubmitField('Send')

class Notes(FlaskForm):
    note = TextAreaField('Note')
    save = SubmitField('Save')

class Profile(FlaskForm):
    password = PasswordField('password')
    save = SubmitField('Save')
        
    