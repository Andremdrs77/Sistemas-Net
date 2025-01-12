from database import get_connection
from datetime import datetime, timedelta


class Loan:
    def __init__(self, book_id, user_id):
        self.data_emprestimo = datetime.now()
        self.data_devolucao = self.data_emprestimo + timedelta(days=14)
        self.book_id = book_id
        self.user_id = user_id



    def save(self):
        conn = get_connection()
        conn.execute("INSERT INTO loans(data_emprestimo, data_devolucao, book_id, user_id) values(?,?,?,?)", (self.data_emprestimo, self.data_devolucao, self.book_id, self.user_id))
        conn.execute("UPDATE books SET disponivel = 0  WHERE id = ?", (self.book_id,))
        conn.commit()
        conn.close()
        return True


    @classmethod
    def all(cls):
        conn = get_connection()
        loans = conn.execute("""SELECT loans.id AS loan_id, books.id AS book_id, books.titulo, users.nome, loans.data_emprestimo, loans.data_devolucao 
FROM loans JOIN books ON loans.book_id = books.id JOIN users ON loans.user_id = users.id""").fetchall()
        conn.close()
        return [dict(loan) for loan in loans]
    

    @classmethod
    def return_book(cls, loan_id, book_id):
        conn = get_connection()
        conn.execute("DELETE FROM loans WHERE id = ?", (loan_id,))
        conn.execute("UPDATE books SET disponivel = 1 WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()