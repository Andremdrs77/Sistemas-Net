from sqlalchemy.orm import Mapped, mappedcolumn, DeclarativeBase
from sqlalchemy import String, ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mappedcolumn(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(50), unique=True)

    def repr(self) -> str:
        return f"(User={self.nome})"

class Receita(Base):
    __tablename__ = 'recites'
    id:Mapped[int] = mapped_column(primary_key=True)
    nome:Mapped[str]
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))