from flask import Flask, request, render_template, session, redirect, url_for, make_response
import sqlite3

DATABASE = 'usuarios.db'
def conectar_banco():
    return sqlite3.connect(DATABASE)

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL,
                   password TEXT NOT NULL,
                   nome TEXT NOT NULL )''')
    
    conn.commit()
    conn.close()

criar_tabela()

app = Flask(__name__)
app.secret_key = 'chave-secreta' # Necessário para gerenciar sessões


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nome = request.form['nome']

        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO usuarios (username, password, nome) VALUES (?, ?, ?)''', (username, password, nome))
            
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        
        except sqlite3.IntegrityError:
            return render_template('register.html', erro='Usuário já cadastrado.')
    
    return render_template('register.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM usuarios WHERE username = ? AND password = ?''', (username, password))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            session['username'] = username
            resposta = make_response(redirect(url_for('dashboard')))
            resposta.set_cookie('username', username, max_age=60 * 60 * 24)
            return resposta
        
        return render_template('login.html', erro='Usuário ou senha incorretos!')
    
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Verificar se usuário está na sessão.
    username = session.get('username') 
    if not username:
        return redirect(url_for('login')) # Redireciona para login se não estiver logado.
    
    return render_template('dashboard.html', username=username)


@app.route('/users')
def list_users():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT nome, username FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()

    return render_template('users.html', usuarios=usuarios)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None) # Remover o usuário da sessão.
    # Remover o cookie
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', max_age=0) # Limpa o cookie.
    return resposta