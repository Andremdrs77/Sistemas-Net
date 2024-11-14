from flask import Flask, request, render_template, \
    redirect, url_for, flash
import sqlite3, os.path
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from flask_sqlalchemy import SQLAlchemy

DATABASE = 'database.db'

app = Flask(__name__)

# habilitar mensagens flash
app.config['SECRET_KEY'] = 'muitodificil'

# obtém conexão com o banco de dados
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.all()
    return render_template("pages/index.html", users=users)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        email = request.form['email']
        senha= request.form['password']

        if not email:
            flash('Email é obrigatório')
        else:
            user = User(email=email, senha=senha)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
    
    return render_template('pages/create.html')

@app.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit(id):

    # obter informação do usuário
    user = User.query.get(id)

    if user == None:
        return redirect(url_for('error', message='Usuário Inexistente'))

    if request.method == 'POST':
        email = request.form['email']
        user.email = email
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('pages/edit.html', user=user)

@app.route('/error')
def error():
    error = request.args.get('message')
    return render_template('errors/error.html', message=error)
