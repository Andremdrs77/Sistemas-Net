from flask import Flask, render_template, url_for, request, redirect
import sqlite3

app = Flask(__name__)

def obter_conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/create', methods=['GET','POST'])
def create_user():
    if request.method == 'POST':
        nome = request.form['nome']
        conn = obter_conexao()
        conn.execute("INSERT INTO usuarios(nome) VALUES(?)", (nome,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar'))

    return render_template('pages/create-user.html')

@app.route('/create_peca', methods=['POST', 'GET'])
def create_peca():
    if request.method == 'POST':
        titulo = request.form['titulo']
        conn = obter_conexao()
        conn.execute("INSERT INTO pecas(titulo) VALUES(?)", (titulo,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_pecas'))
    return render_template('pages/create-pecas.html')

@app.route('/create_danca', methods=['POST', 'GET'])
def create_danca():
    if request.method == 'POST':
        titulo = request.form['titulo']
        conn = obter_conexao()
        conn.execute("INSERT INTO dancas(titulo) VALUES(?)", (titulo,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_dancas'))
    return render_template('pages/create-dancas.html')
    
@app.route('/listar-usuario')
def listar():
    conn = obter_conexao()
    users = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return render_template('pages/listar-users.html', users = users)

@app.route('/<int:id>/listar_peca')
def listar_peca(id):
    conn = obter_conexao()
    peca = conn.execute("SELECT * FROM pecas WHERE id = ?", (id,)).fetchone()
    conn.close()
    if peca:
        return render_template('pages/show-peca.html', peca=peca)
    return "Esta peça não existe";    

@app.route('/<int:id>/listar_danca')
def listar_danca(id):
    conn = obter_conexao()
    danca = conn.execute("SELECT * FROM dancas WHERE id = ?", (id,)).fetchone()
    conn.close()
    if danca:
        return render_template('pages/show-danca.html', danca=danca)
    return "Esta dança não existe";    

@app.route('/<int:id>/listar-usuarios')
def listar_user(id):
    conn = obter_conexao()
    user = conn.execute("SELECT * FROM usuarios WHERE id = ?", (id,)).fetchone()
    conn.close()
    if user:
        return render_template('pages/show-user.html', user=user)        
    return "Usuário não encontrado"

@app.route('/listar-pecas')
def listar_pecas():
    conn = obter_conexao()
    pecas = conn.execute('SELECT * FROM pecas').fetchall()
    conn.close()
    return render_template('pages/listar-pecas.html', pecas=pecas)

@app.route('/listar-dancas')
def listar_dancas():
    conn = obter_conexao()
    dancas = conn.execute('SELECT * FROM dancas').fetchall()
    conn.close()
    return render_template('pages/listar-dancas.html', dancas=dancas)

@app.route('/<int:id>/deletar-peca')
def deletar_peca(id):
    conn = obter_conexao()
    peca = conn.execute("SELECT * FROM pecas WHERE id = ?", (id,)).fetchone()
    if peca:
        conn.execute("DELETE FROM pecas WHERE id = ?", (id,))
        conn.commit()
    conn.close()
    return redirect(url_for('listar_pecas'))

    