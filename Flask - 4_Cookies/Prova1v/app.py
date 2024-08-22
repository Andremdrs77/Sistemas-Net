from flask import Flask, render_template, request, make_response, url_for, redirect

app = Flask(__name__)
ListaResultados = []

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        NomeUsuario = request.form.get('nome')
        response = make_response(redirect(url_for('formulario')))
        response.set_cookie('usuario', NomeUsuario)
        return response

    if request.method =='GET':
        return render_template('login.html')

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    usuario = request.cookies.get('usuario')

    if not usuario:
        return redirect(url_for('login'))

    
    tempo = request.args.get('tempo')
    distancia = request.args.get('distancia')
    if tempo and distancia:
        ListaResultados.append({'nome': usuario, 'tempo': tempo, 'distancia': distancia})
        return redirect(url_for('formulario'))

    resultados_usuario = [resultado for resultado in ListaResultados if resultado['nome'] == usuario]
    return render_template('formulario.html', resultados_usuario=resultados_usuario, usuario=usuario)