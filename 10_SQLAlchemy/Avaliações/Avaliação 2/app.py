from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicialização do app Flask e configuração do banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///florista.db'  # Banco SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos do banco de dados
class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    rg = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    pedidos = db.relationship('Pedido', back_populates='cliente', cascade='all, delete-orphan')

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    pedidos = db.relationship('PedidoProduto', back_populates='produto', cascade='all, delete-orphan')

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    cliente = db.relationship('Cliente', back_populates='pedidos')
    itens = db.relationship('PedidoProduto', back_populates='pedido', cascade='all, delete-orphan')

class PedidoProduto(db.Model):
    __tablename__ = 'pedido_produto'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    pedido = db.relationship('Pedido', back_populates='itens')
    produto = db.relationship('Produto', back_populates='pedidos')

# Criação do banco de dados
with app.app_context():
    db.create_all()

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    pedidos = Pedido.query.all()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/cadastrar-cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        rg = request.form.get('rg')
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')

        novo_cliente = Cliente(rg=rg, nome=nome, telefone=telefone)
        db.session.add(novo_cliente)
        db.session.commit()
        return "Cliente cadastrado com sucesso!"
    return render_template('cadastrar_cliente.html')

@app.route('/cadastrar-produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form.get('nome')
        tipo = request.form.get('tipo')
        preco = request.form.get('preco')

        novo_produto = Produto(nome=nome, tipo=tipo, preco=float(preco))
        db.session.add(novo_produto)
        db.session.commit()
        return "Produto cadastrado com sucesso!"
    return render_template('cadastrar_produto.html')

@app.route('/cadastrar-pedido', methods=['GET', 'POST'])
def registrar_pedido():
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        produtos = request.form.get('produtos').split(',')  # Lista no formato "1:2,3:4"

        novo_pedido = Pedido(cliente_id=int(cliente_id))
        db.session.add(novo_pedido)
        db.session.flush()

        for item in produtos:
            produto_id, quantidade = map(int, item.split(':'))
            novo_item = PedidoProduto(pedido_id=novo_pedido.id, produto_id=produto_id, quantidade=quantidade)
            db.session.add(novo_item)

        db.session.commit()
        return "Pedido registrado com sucesso!"
    return render_template('cadastrar_pedido.html')
