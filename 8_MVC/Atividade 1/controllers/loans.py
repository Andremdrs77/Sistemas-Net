from flask import Flask, render_template, url_for, request, Blueprint, redirect, flash
from models.user import User
from models.loan import Loan
from models.book import Book

bp = Blueprint('loans', __name__, url_prefix='/loans')

@bp.route('/')
def index():
    return render_template('loans/index.html', loans=Loan.all())

@bp.route('/register', methods=['POST', 'GET'])
def register():
    
    if request.method == 'POST':
        book_id = request.form['book']
        user_id = request.form['user']

        if not user_id or not book_id:
            flash('É necessário registrar usuário e livro.')
        else:
            loan = Loan(book_id, user_id)
            loan.save()
            return redirect(url_for('loans.index'))


    users = User.all()
    books = Book.available()
    return render_template('loans/register.html', users=users, books=books)


@bp.route('/return/<int:loan_id>/<int:book_id>')
def return_book(loan_id, book_id):
    Loan.return_book(loan_id, book_id)
    flash('Livro devolvido!')
    return redirect(url_for('loans.index'))