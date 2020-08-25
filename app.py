#SE Project Email program Willam Giddens, Trey O'neal, Joe Howard, Chad Whitney

from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ourseecretkeyz1112'


@app.route('/')
def default():
    return render_template('default.html')

@app.route('/login')
def login():
    return render_template('login.html')

app.run(debug=True, host ='0.0.0.0')