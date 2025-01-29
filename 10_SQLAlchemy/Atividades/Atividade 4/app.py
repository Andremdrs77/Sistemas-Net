from flask import Flask, request, render_template_string, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locadora.db'
db = SQLAlchemy(app)

# Modelos
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    placa = db.Column(db.String(10), unique=True, nullable=False)

class Locacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
    data_locacao = db.Column(db.String(10), nullable=False)
    data_devolucao = db.Column(db.String(10), nullable=False)
    
    cliente = db.relationship('Cliente', backref=db.backref('locacoes', lazy=True))
    veiculo = db.relationship('Veiculo', backref=db.backref('locacoes', lazy=True))

@app.route('/cadastrar_cliente', methods=['POST'])
def cadastrar_cliente():
    nome = request.form['nome']
    telefone = request.form['telefone']
    cliente = Cliente(nome=nome, telefone=telefone)
    db.session.add(cliente)
    db.session.commit()
    return redirect(url_for('listar_clientes'))

@app.route('/cadastrar_veiculo', methods=['GET', 'POST'])
def cadastrar_veiculo():
    if request.method == 'POST':
        modelo = request.form['modelo']
        placa = request.form['placa']
        veiculo = Veiculo(modelo=modelo, placa=placa)
        db.session.add(veiculo)
        db.session.commit()
        return redirect(url_for('listar_veiculos'))
    
    return render_template('cadastrar_veiculo.html')

@app.route('/cadastrar_locacao', methods=['GET', 'POST'])
def cadastrar_locacao():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        veiculo_id = request.form['veiculo_id']
        data_locacao = request.form['data_locacao']
        data_devolucao = request.form['data_devolucao']
        locacao = Locacao(cliente_id=cliente_id, veiculo_id=veiculo_id, 
                          data_locacao=data_locacao, data_devolucao=data_devolucao)
        db.session.add(locacao)
        db.session.commit()
        return redirect(url_for('listar_locacoes'))
    
    clientes = Cliente.query.all()
    veiculos = Veiculo.query.all()
    return render_template('cadastrar_locacao.html', clientes=clientes, veiculos=veiculos)

@app.route('/listar_clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template_string('<ul>{% for c in clientes %}<li>{{ c.nome }} - {{ c.telefone }}</li>{% endfor %}</ul>', clientes=clientes)

@app.route('/listar_veiculos', methods=['GET'])
def listar_veiculos():
    veiculos = Veiculo.query.all()
    return render_template_string('<ul>{% for v in veiculos %}<li>{{ v.modelo }} - {{ v.placa }}</li>{% endfor %}</ul>', veiculos=veiculos)

@app.route('/listar_locacoes', methods=['GET'])
def listar_locacoes():
    locacoes = Locacao.query.all()
    return render_template_string('<ul>{% for l in locacoes %}<li>{{ l.cliente.nome }} alugou {{ l.veiculo.modelo }} de {{ l.data_locacao }} até {{ l.data_devolucao }}</li>{% endfor %}</ul>', locacoes=locacoes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

