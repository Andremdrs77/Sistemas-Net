from flask import Flask, render_template
from users import users
from books import books
from auth import bp
from users.models import User
from flask_login import LoginManager

app = Flask (__name__, template_folder='templates')


app.config['SECRET_KEY']= 'SUPERDIFICIL'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.find(id=user_id)

app.register_blueprint(users.bp)
app.register_blueprint(books.bp)
app.register_blueprint(bp.auth_bp)


@app.route('/')
def index():
    return render_template('layout.html')


