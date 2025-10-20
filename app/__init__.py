from flask import Flask, redirect, url_for
from app.users.routes import users_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'

    app.register_blueprint(users_bp, url_prefix='/users')

    # Головна сторінка одразу перенаправляє на логін
    @app.route('/')
    def home():
        return redirect(url_for('users.login'))

    return app
