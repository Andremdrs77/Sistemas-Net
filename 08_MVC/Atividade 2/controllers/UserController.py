from flask import Flask, render_template, url_for, redirect, request, flash
from .. import app
from ..database import get_connection
from ..models.user import User


@app.route('/')
def index():
    conn = get_connection()    
    users = conn.execute("SELECT * FROM users").fetchall()
    return render_template('index.html', users = users)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        nome= request.form['nome']

        if not email:
            flash('Email é obrigatório')
        else:
            conn = get_connection()
            conn.execute("INSERT INTO users(email, nome) VALUES (?,?)", (email, nome))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('register.html')