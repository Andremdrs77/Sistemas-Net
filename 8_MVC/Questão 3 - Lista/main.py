from database import create_db, get_connection, save
from models.modelo1 import Classe1
from models.modelo2 import Classe2

if __name__ == '__main__':
    # a função create db invoca o acesso a conexão via get_connection
    create_db('database.db', 'database.sql')
    
    c1 = Classe1('João', 'Classe 1')
    save(c1, 'database.db')
    
    c2 = Classe2('Vasco', 'Classe 2')
    save(c2, 'database.db')


