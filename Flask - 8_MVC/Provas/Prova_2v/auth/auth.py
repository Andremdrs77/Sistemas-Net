from flask import render_template, Blueprint, url_for, request, flash, redirect

# módulo de usuários
bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')

@bp.route('/login')
def login():
    return render_template('login.html')