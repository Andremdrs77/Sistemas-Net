from flask import Flask, render_template, request, redirect, url_for
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
        user = User(nome=request.form['nome'])
        session.add(user)
        session.commit()

        return redirect(url_for('index'))

    users = session.query(User).all()
    return render_template('index.html', users=users)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = session.query(User).get(id)

    if request.method == 'POST':
        user.nome = request.form['nome']
        session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', user=user)


@app.route('/remove/<int:id>', methods=['GET', 'POST'])
def remove(id):
    user = session.query(User).get(id)

    if user:
        session.delete(user)
        session.commit()

    return redirect(url_for('index'))
