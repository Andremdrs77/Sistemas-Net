from flask import Blueprint

bp = Blueprint(
    name='user',
    import_name=__name__,
    url_prefix='/user'
)

@bp.route('/')
def index():
    return 'USER_BP'

@bp.route('/register')
def register():
    return 'register'