from sqlalchemy.orm import *
from sqlalchemy import *

class Base(DeclarativeBase):
    pass

# mapeamento declarativo
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    nome: Mapped[str]

    def __repr__(self):
        return f"Nome = {self.nome}, Email = {self.email}"
    
class Book(Base):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    dono: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
# fabricar conexão
engine = create_engine("sqlite:///teste.db")
Session = sessionmaker(bind=engine)
session = Session()

# criar o banco
Base.metadata.create_all(engine)

# criado o objeto
us1 = User(nome="Velma", email="velma@velma.com")
session.add(us1)
session.commit()

# sql_email = select(User.email).where(User.email == "velma@velma.com")
# print(sql_email)

sql = select(User)
lista = session.execute(sql).all()
print(lista)

us2 = User(nome='eu', email='eu@mesmo.com')
sql = insert(User).values(email='eu@mesmo.com')
