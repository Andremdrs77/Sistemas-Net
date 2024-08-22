from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1><a href='/dashboard'>Dashboard</a> <br/> <a href='/profile'>Profile</a></h1>"

@app.route('/dashboard')
def dashboard():
   return render_template('dashboard.html')

@app.route('/profile')
def profile():
   return render_template('profile.html')