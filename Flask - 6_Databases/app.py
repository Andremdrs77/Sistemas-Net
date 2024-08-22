from flask import Flask, render_template, url_for, flash, redirect, request
import sqlite3

app = Flask(__name__)

def get_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conexao = get_connection()
    lista = conexao.execute("SELECT id, email FROM users").fetchall()
    return render_template('pages/index.html', users=lista)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']
        conexao = get_connection()
        SQL=f"INSERT INTO users (email, senha) VALUES ('{email}','{senha}')"
        conexao.execute(SQL)
        conexao.commit()
        conexao.close()
        return redirect(url_for('index'))
        
    
    return render_template('pages/create.html')