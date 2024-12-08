from flask import Flask, request, render_template, session, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = 'chave-secreta' # Necessário para gerenciar sessões

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin': # User e Senha pré-definidos!
            session['username'] = username

            resposta = make_response(redirect(url_for('dashboard')))
            resposta.set_cookie('username', username, max_age=60 * 60 * 24) #Cookie válido por 1 dia.

            return resposta
        else:
            return render_template('login.html', erro='Usuário ou senha inválidos!')
        
    if 'username' in session: # Verificar se usuário já está logado.
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # Verificar se usuário está na sessão.
    username = session.get('username') 
    if not username:
        return redirect(url_for('login')) # Redireciona para login se não estiver logado.
    
    return render_template('dashboard.html', username=username)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None) # Remover o usuário da sessão.
    # Remover o cookie
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', max_age=0) # Limpa o cookie.
    return resposta


