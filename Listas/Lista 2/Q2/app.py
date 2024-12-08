from flask import Flask, request, render_template, session, redirect, url_for, make_response

usuarios_registrados = []

app = Flask(__name__)
app.secret_key = 'chave-secreta' # Necessário para gerenciar sessões


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nome = request.form['nome']

        # Verificar se o usuário ja foi cadastrado.
        for usuario in usuarios_registrados:
            if usuario['username'] == username:
                return render_template('register.html', erro='Usuário ja cadastrado!')
            
        # Adicionar novo usuario à lista.
        usuarios_registrados.append({
            'username': username,
            'password': password,
            'nome': nome
        })

        return redirect(url_for('login'))
    
    return render_template('register.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for usuario in usuarios_registrados:
            if usuario['username'] == username and usuario['password'] == usuario['password']:
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
    
    return render_template('users.html', usuarios=usuarios_registrados)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None) # Remover o usuário da sessão.
    # Remover o cookie
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', max_age=0) # Limpa o cookie.
    return resposta