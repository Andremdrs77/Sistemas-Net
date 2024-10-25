from database import get_connection
from datetime import datetime, timedelta

class Loan:
    def __init__(self, book_id, user_id):
        self.data_emprestimo = datetime.now
        self.data_devolucao = self.data_emprestimo + timedelta(days=14)
        self.book_id = book_id
        self.user_id = user_id

    def save(self):
        conn = get_connection()
        conn.execute("INSERT INTO loans(data_emprestimo, data_devolucao, book_id, user_id) values(?,?,?,?)", (self.data_emprestimo, self.data_devolucao, self.book_id, self.user_id))
        conn.commit()
        conn.close()
        return True
    
    @classmethod
    def all(cls):
        conn = get_connection()
        loans = conn.execute("SELECT ")