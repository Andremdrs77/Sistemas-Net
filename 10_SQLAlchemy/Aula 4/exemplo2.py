from database.config import start_db, destroy_db, session
from database.models import User, Receita
from random import randint

start_db()


user = User(nome='sheldon')
session.add(user)
session.commit()

receita1 = Receita(nome='papa', user_id=user.id)
receita2 = Receita(nome='stronogofonoff', user_id=user.id)
session.add_all( [receita1, receita2] )
session.commit()

# re = session.query(Receita).first()
# print(re.nome)
# print(re.id)
# print(re.user_id)
print(user.receitas)

# user2 = session.query(User).get(randint(101, 101)) # Versão 1
user2 = session.get(User, randint(101, 101)) # Versão 2

print(user2)
print(user2.receitas)