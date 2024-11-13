from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, session
from sqlalchemy import create_engine, select

class Base(DeclarativeBase):
    pass

# mapeamento declarativo
class User(Base):
    ___tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    nome: Mapped[str] = mapped_column()

    def __retr__(self):
        return f"Nme = {self.nome}, Email = {self.email}"
    
# fabricar conexão
engine = create_engine("sqlite:///teste.db")

# criar o banco
Base.metadata.create_all(engine)

# criado o objeto
us1 = User(nome="Velma", email="velma@velma.com")
session.add(us1)
session.commit()

sql_email = select(User.email).where(User.email == "velma@velma.com")
print(sql_email)