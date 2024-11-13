from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, logout_user, login_user
from users.models import User 

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')

login_manager = LoginManager()
login_manager.init_app(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.find(id=user_id)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']

        user = User.find(email=email)

        if user:
            login_user(user)

            return redirect(url_for('users.index'))
        else:
            return render_template('auth/login.html') + '<br/><h3 style= "color: red">Usuário não encontrado</h3>'
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']

        user = User(nome, email)
        user.save()

        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
   # usa o método do Flask-Login para limpar a sessão do usuário.
   logout_user()
   return redirect(url_for('auth.login'))