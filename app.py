#SE Project Email program Willam Giddens, Trey O'neal, Joe Howard, Chad Whitney
import creds
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, Search, ComposeEmail
from nylas import APIClient
from flask_wtf.csrf import CSRFProtect

temdb = 'mysql://'+ creds.sql_username + ':' + creds.sql_password + '@' + creds.sql_host + '/' + creds.sql_database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ourseecretkeyz1112'
app.config['WTF_CSRF_SECRET_KEY'] = 'ourseecretkeyz1112'
app.config['SQLALCHEMY_DATATBASE_URI'] = temdb
csrf = CSRFProtect(app)

db= SQLAlchemy(app)
login_manager = LoginManager()

class USER(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have Been Logged Out!', 'success')
    return redirect(url_for('default'))

@app.route('/')
def default():
    return render_template('default.html')

## This is the login route

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@test.com' and form.password.data == 'thegoonies':
            flash('You have Been Logged In!', 'success')
            return redirect(url_for('email'))
        else:
            flash('Login Failed, Please Check Your Credentials and Try Again', 'danger')
    return render_template('default1.html', title='Login', form=form)

## This route shows succesful login

@app.route('/success')
def default1():
    return render_template('default1.html')   

## This route shows current emails

@app.route("/email/", methods=['GET', 'POST'])
def email():
    from nylas import APIClient
  
    nylas = APIClient(    creds.CLIENT_ID,
    creds.CLIENT_SECRET,
    creds.ACCESS_TOKEN    
    )

    data = nylas.messages.all()

    return render_template("email.html", data=data)

## This route searches emails and returns emails found

@app.route("/email-search/", methods=['GET', 'POST'])
def emailsearch():
    from nylas import APIClient
    
    
    nylas = APIClient(    creds.CLIENT_ID,
    creds.CLIENT_SECRET,
    creds.ACCESS_TOKEN    
    )

    data = Search("chad")


    return render_template("email-search.html", data=data)

## This route shows individual emails

@app.route("/emails/<id>", methods=['GET', 'POST'])
def emails(id):
    from nylas import APIClient
  
    nylas = APIClient(    creds.CLIENT_ID,
    creds.CLIENT_SECRET,
    creds.ACCESS_TOKEN    
    )

    data = nylas.messages.get(id)

    
    if not data.files:
        data.files = "none"


    return render_template("emails.html", data=data)
         
@app.route("/compose/", methods=['GET', 'POST'])

def compose():
    
    from nylas import APIClient
    form = ComposeEmail()
    print("hello chad")

    if form.is_submitted():
        print("submitted")
        print(form.data)

    if form.validate():
        print("valid")

    print(form.errors)
    
    
    
    if form.validate_on_submit():
        print("hello world")
        
        nylas = APIClient(creds.CLIENT_ID,
        creds.CLIENT_SECRET,
        creds.ACCESS_TOKEN    
        )
        print(form.data)
        draft = nylas.drafts.create()
        # draft.subject = "With Love, from Nylas"
        # draft.body = "This email was sent using the Nylas Email API. Visit https://nylas.com for details."
        # draft.to = [{'name': 'My Nylas Friend', 'email': 'swag@nylas.com'}]
        data = form.data
        print(data['body'])
        draft.subject = data['subject']
        draft.to = [{'email': data['to']}]
        draft.body = data['body']
        draft.send()
        flash('Email Sent', 'success')

    else:                   
        return render_template("compose.html", form=form)                    
    return render_template("compose.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





app.run(debug=True, host ='0.0.0.0')

# class ComposeEmail(FlaskForm):
#     to = StringField('email', validators=[DataRequired(),Email()])
#     cc = StringField('email', validators=[DataRequired(),Email()])
#     bcc = StringField('email', validators=[DataRequired(),Email()])
#     subject = StringField()
#     body = StringField()
#     submit = SubmitField('Send')
