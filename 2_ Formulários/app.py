from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Oi</h1>"

@app.route('/render')
def render():
    return render_template('render.html')

@app.route('/dados')
def dados():
    nome = 'Romerito sucks'
    return render_template('dados.html', nome=nome)

@app.route('/formulario', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('formulario.html')
    else:
        nome = request.form['nome']
        return render_template('dados.html', nome=nome)