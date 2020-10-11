# SE Project Email program Willam Giddens, Trey O'neal, Joe Howard, Chad Whitney
import creds
import os
import tempfile
from flask import Flask, abort, render_template, url_for, flash, redirect, request, session, g , send_file
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, Search, ComposeEmail
from nylas import APIClient
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt


# configures the flask ap
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ourseecretkeyz1112'
app.config['WTF_CSRF_SECRET_KEY'] = 'ourseecretkeyz1112'
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)




class User:
    def __init__(self, id, username, password):
        self.id = id
        self.email_address = email_address
        self.password = password

    def __repr__(self):
        return f'<User: {self.email_address}>'




# isUserValid takes in email_address and password then returns on whether or not a user's credentials are valid

def isUserValid(email, candidate):
    
    id = getUserId(email)
    print(id)
    if id == -1:
        return (False,-1)
    
    config = {
        'user': creds.sql_username,
        'password': creds.sql_password,
        'host': creds.sql_host,
        'port': creds.sql_port,
        'database': creds.sql_database
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = ("SELECT * FROM user WHERE id =" + str(id))
    print("in is valid")
    print(query)

    cursor.execute(query)
    print(cursor)
    for item in cursor:
        print(item)
        temphash = item[2]


    cursor.close()
    connection.close()

    return (bcrypt.check_password_hash(temphash, candidate),id) 

## getUserId takes in an email address and returns a valid id or a -1 if email not found
def getUserId(email_address):
    config = {
        'user': creds.sql_username,
        'password': creds.sql_password,
        'host': creds.sql_host,
        'port': creds.sql_port,
        'database': creds.sql_database
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = ("SELECT * FROM user")
    cursor.execute(query)
    
    for item in cursor:     
        if item[1] == email_address:
            return item[0]
    
    cursor.close()
    connection.close()

    return -1    


# Sets the default route for the application
@app.route('/')
def default():
    
    return redirect(url_for('login'))


# This is the login route

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    session.pop('id', None)
    if request.method == 'POST':
        
        if form.validate_on_submit():
            validate = isUserValid(form.email.data, form.password.data)
            if validate[0] == False:
                flash('Login Failed, Please Check Your Credentials and Try Again', 'danger')
           
            else:
                session['id'] = validate[1]
                flash('You have Been Logged In!', 'success')
                return redirect(url_for('email'))
                
    
    return render_template('default1.html', title='Login', form=form)

# This route shows succesful login

@app.route('/success')
def default1():
    return render_template('default1.html')   


# sets the logout route
@app.route('/logout')

def logout():
    
    session.pop('id', None)
    session.pop('csrf_token', None)
    flash('You have Been Logged Out!', 'success')
    return redirect(url_for('login'))


# This route shows current emails

@app.route("/email/", methods=['GET', 'POST'])
def email():
    from nylas import APIClient
    
    nylas = APIClient(    creds.CLIENT_ID,
        creds.CLIENT_SECRET,
        creds.ACCESS_TOKEN    
        )
    form = Search()
    if 'query' in request.args :
        query = request.args.get('query')
        print( query)
        data = nylas.messages.search(query)
        return render_template("email.html", form=form, data=data)
    else:
        data = nylas.messages.all()

    return render_template("email.html", form=form, data=data)

# This route searches emails and returns emails found

@app.route("/email-search/", methods=['GET', 'POST'])
def emailsearch():
    # # class Search():
    # query = StringField('query')
    # submit = SubmitField('Search')
    
    form = Search()

    from nylas import APIClient

    nylas = APIClient(    creds.CLIENT_ID,
    creds.CLIENT_SECRET,
    creds.ACCESS_TOKEN    
    )

    data = Search(form.query.data)
    print

    return render_template("emails.html", data=data)


# This route shows individual emails


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
         
@app.route("/download/<id>", methods=['GET'])
def download(id):
    
    
    from nylas import APIClient
  
    nylas = APIClient(    creds.CLIENT_ID,
    creds.CLIENT_SECRET,
    creds.ACCESS_TOKEN    
    )


    # Replace {id} with the appropriate file id
    file = nylas.files.get(id)
    root = os.path.abspath(os.curdir)
    filename = root + '/static/download/' + file['filename']
    temp = open(filename, 'w+b')
    temp.write(file.download())
    temp.close()    
    
 
    return send_file(filename, as_attachment=True, attachment_filename=file['filename'], mimetype=file['content_type'])
    
    
# Sets the route for composing a new email
@app.route("/compose/", methods=['GET', 'POST'])

def compose():
    
    
    from nylas import APIClient
    form = ComposeEmail()    
    if request.method == 'POST':

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

@app.before_request
def before_request():
    print(session)
    if 'id' not in session and request.endpoint != 'login':
        return redirect(url_for('login'))
    


app.run(debug=True, host ='0.0.0.0')
