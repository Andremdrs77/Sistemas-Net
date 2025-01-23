from sqlalchemy import create_engine, Table, Column, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, mapped_column, Mapped

engine = create_engine('sqlite:///exemplo1.db')
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass


estudante_curso = Table(
    "estudantes_cursos",
    Base.metadata,
    Column('estudante_id', ForeignKey('estudantes.id'), primary_key=True),
    Column('curso_id', ForeignKey('cursos.id'), primary_key=True)
)
# relacionamento NxN


class Curso(Base):
    __tablename__ = 'cursos'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)


class Estudante(Base):
    __tablename__ = 'estudantes'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
