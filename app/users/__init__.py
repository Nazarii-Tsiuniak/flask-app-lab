from flask import Blueprint

users_bp = Blueprint('users_bp', __name__, url_prefix='/users')

@users_bp.route('/hi/<name>')
def greetings(name):
    return f"Привіт, {name}!"

@users_bp.route('/admin')
def admin():
    return "Сторінка адміністратора"
