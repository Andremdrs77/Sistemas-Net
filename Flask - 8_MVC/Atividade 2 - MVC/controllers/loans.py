from flask import Flask, render_template, url_for, request, Blueprint, redirect
from models.user import User
from models.loan import Loan

bp = Blueprint('loans', __name__, url_prefix='/loans')

@bp.route('/')
def index():
    return render_template('loans/index.html', loans=Loan.all())

@bp.route('/register', methods=['POST', 'GET'])
def register():
    
    if request.method == 'POST':
        book = request.form['book']
        user = request.form['user']

        loan = Loan(book, user)
        loan.save()
        return redirect(url_for('loans.index'))


    return render_template('loans/register.html', loans=Loan.all())