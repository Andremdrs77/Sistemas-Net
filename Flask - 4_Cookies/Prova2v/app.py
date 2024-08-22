from flask import Flask, render_template, request, make_response, url_for, redirect

app = Flask(__name__)
ListaMensagens = []

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        NomeUsuario = request.form.get('nome')
        response = make_response(redirect(url_for('mensagem')))
        response.set_cookie('usuario', NomeUsuario)
        return response

    if request.method =='GET':
        return render_template('login.html')

@app.route('/mensagem', methods=['GET', 'POST'])
def mensagem():
    usuario = request.cookies.get('usuario')

    if not usuario:
        return redirect(url_for('login'))

    if request.method == 'POST':
        mensagem = request.form.get('texto')
        if mensagem:
            ListaMensagens.append({'nome': usuario, 'mensagem': mensagem})

    mensagens_usuario = [mensagem for mensagem in ListaMensagens if mensagem['nome'] == usuario]
    return render_template('mensagem.html', mensagens_usuario=mensagens_usuario, usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)