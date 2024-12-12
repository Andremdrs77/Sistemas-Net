from database.config import start_db, destroy_db, session
from database.models import User

start_db()


user = User(nome='bill')
session.add(user)
session.commit()

receita1 = Receita(nome='papa')
session.add(receita1)
session.commit()
