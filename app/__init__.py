from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.users.views import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    @app.route('/')
    def index():
        return '<h1>Головна сторінка</h1><p><a href="/users/hi/John?age=30">Перейдіть на /users/hi/John</a></p>'

    return app
