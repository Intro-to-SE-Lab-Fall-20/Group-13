#SE Project Email program Willam Giddens, Trey O'neal, Joe Howard, Chad Whitney

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
    CLIENT_ID='erta7s4vw61q37aw14wx1f7kv'
    ACCESS_TOKEN='GD7S4grE0FruLFBm2TiixeyLY3YoGC'
    CLIENT_SECRET='1coubzlaae6c0irdoyya36qby'
    nylas = APIClient(    CLIENT_ID,
    CLIENT_SECRET,
    ACCESS_TOKEN    
    )

    data = nylas.messages.all()




    return render_template("email.html", data=data)


@app.route("/email-search/", methods=['GET', 'POST'])
def emailsearch():
    from nylas import APIClient
    
    nylas = APIClient(    CLIENT_ID,
    CLIENT_SECRET,
    ACCESS_TOKEN    
    )

    data = nylas.messages.search("hit")




    return render_template("email-search.html", data=data)


         

app.run(debug=True, host ='0.0.0.0')