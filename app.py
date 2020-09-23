#SE Project Email program Willam Giddens, Trey O'neal, Joe Howard, Chad Whitney
import creds
from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm
from nylas import APIClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ourseecretkeyz1112'


@app.route('/')
def default():
    return render_template('default.html')

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

@app.route('/success')
def default1():
    return render_template('default1.html')   

@app.route("/email/", methods=['GET', 'POST'])
def email():
    from nylas import APIClient
  
    nylas = APIClient(    creds.CLIENT_ID,
    creds.CLIENT_SECRET,
    creds.ACCESS_TOKEN    
    )

    data = nylas.messages.all()




    return render_template("email.html", data=data)


@app.route("/email-search/", methods=['GET', 'POST'])
def emailsearch():
    from nylas import APIClient
    
    nylas = APIClient(    creds.CLIENT_ID,
    creds.CLIENT_SECRET,
    creds.ACCESS_TOKEN    
    )

    data = nylas.messages.search("chad")




    return render_template("email-search.html", data=data)

@app.route("/emails/{id}", methods=['GET', 'POST'])
def emailsearch():
    from nylas import APIClient
  
    nylas = APIClient(    creds.CLIENT_ID,
    creds.CLIENT_SECRET,
    creds.ACCESS_TOKEN    
    )

    data = nylas.messages.get('{id}')




    return render_template("emails.html", data=data)
         

app.run(debug=True, host ='0.0.0.0')