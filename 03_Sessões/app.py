from flask import Flask, request, render_template, url_for, session, redirect

app = Flask(__name__)

bancodados = []
app.config['SECRET KEY'] = 'superdificil'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():

    # session['user'] = 'romerito'
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    return "LOGIN"

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        nome = request.form['nome']
        senha = request.form['senha']

        #registrar no banco
        if nome in bancodados:
            return "Já estás cadastrado"
        else:
            bancodados[nome] = senha
            session['user'] = nome
            return redirect(url_for('dashboard'))

    return render_template('register.html')