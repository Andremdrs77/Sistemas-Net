from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5()
bootstrap.init_app(app)

app.config['SECRET'] = 'ROMERITO'

@app.route('/')
def index():
    return render_template('login.html')