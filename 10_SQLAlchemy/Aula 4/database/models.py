from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy import String, ForeignKey
from typing import List

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    nome:Mapped[str] = mapped_column(String(50))
    receitas:Mapped[List['Receita']]=relationship('Receita', backref='user')

    def repr(self) -> str:
        return f"(User={self.nome})"


class Receita(Base):
    __tablename__ = 'recipes'
    id:Mapped[int] = mapped_column(primary_key=True)
    nome:Mapped[str]
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f"(Cumê={self.nome})"

