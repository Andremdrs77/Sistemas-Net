from flask import Blueprint, redirect, url_for

bp = Blueprint(
    name='book',
    import_name=__name__,
    url_prefix='/book'
)

@bp.route('/')
def index():
    return 'book'


@bp.route('/register')
def register():
    return 'register'


@bp.route('/redirect')
def redirect_user():
    return redirect(url_for('user.index'))