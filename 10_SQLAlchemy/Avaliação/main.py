from core.core import core
from auth import login_manager
from auth.routes import auth_bp
from flask import Flask
from sqlalchemy import *
from sqlalchemy.orm import *

# importar Base e engine
from database.models import Base

# Inicializa a apliacação
application = Flask(__name__)
application.config['SECRET_KEY'] = '123123123123'

# criar o banco com Base.medatada.create_all()

# Inicializa o controle de sessões
login_manager.init_app(application)

# Registra as rotas da aplicação
application.register_blueprint(core)

# Registra rotas de login/logout
application.register_blueprint(auth_bp)

# Chama a função para criar o banco de dados
