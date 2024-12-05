from flask import Flask, render_template, request
from sqlalchemy import *
from sqlalchemy.orm import *

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)


#Fabricar conexão
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

#Criar database.db
Base.metadata.create_all(engine)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        session.add(User(nome=nome))
        session.commit()

        users = session.query(User).all()
        return render_template('index.html', users=users)
    
    return render_template('index.html')
