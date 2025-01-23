from slqalchemy import create_engine
from slqalchemy.orm import Session, DeclarativeBase, mapped_column, Mapped

engine = create_engine('sqlite:///exemplo1.db')
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    gerente_id = mapped_column(ForeignKey('users.id'), nullable=True)

    gerenciados: Mapped[List['User']] = relationship('User', back_populates='gerente')
    gerente = relationship('User', back_populates='gerenciados', remote_side=[id])

    def __repr__(self) -> str:
        return self.nome


Base.metadata.create_all(bind=engine)


# user1 = User(nome='John')
# user2 = User(nome='Jane')

# session.add_all([user1, user2])
# session.commit()
# session.close()

sttm = select(User).where(User.id == 1)

chefe = session.execute(sttm).scalars().first()
print(chefe.nome)

# Já conseguimos obter os gerenciados
print(chefe.gerenciados)