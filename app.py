#SE Project Email program Willam Giddens, Trey O'neal, Joe Howard, Chad Whitney
import creds
from flask import Flask, render_template, url_for, flash, redirect, request, session, g
import mysql.connector
from flask_login import LoginManager,UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, Search, ComposeEmail
from nylas import APIClient
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt


#configures the flask ap
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ourseecretkeyz1112'
app.config['WTF_CSRF_SECRET_KEY'] = 'ourseecretkeyz1112'
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()



@app.before_request
def before_request():
    if 'id' in session:
        user = [x for x in users if x.id == session['id']][0]
        g.user = user


class User:
    def __init__(self,id,username,password):
        self.id = id
        self.email_address = email_address
        self.password = password
    
    def __repr__(self):
        return f'<User: {self.email_address}>'


# code get user from database
def getUser(id):
    config = {
        'user': creds.sql_username,
        'password': creds.sql_password,
        'host': creds.sql_host,
        'port': creds.sql_port,
        'database': creds.sql_database
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = ("SELECT * FROM user WHERE id =" + str(id) )
    cursor.execute(query)
    for item in cursor:
        print(item)
    cursor.close()
    connection.close()

def updateUser(id, passw):
    pw_hash = bcrypt.generate_password_hash(passw).decode('utf-8')
    
    config = {
        'user': creds.sql_username,
        'password': creds.sql_password,
        'host': creds.sql_host,
        'port': creds.sql_port,
        'database': creds.sql_database
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = ("UPDATE user SET password = \'" + pw_hash + "\' WHERE id = \'" + str(id)+ "\';" )
    print(query)
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    
    
    
    


## Sets the default route for the application
@app.route('/')
def default():
    
    updateUser(2,"strong")
    getUser(2)
    

      
    return redirect(url_for('login'))


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


##sets the logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have Been Logged Out!', 'success')
    return redirect(url_for('default'))


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
         

## Sets the route for composing a new email
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