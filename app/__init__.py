from flask import Flask

def create_app():
    app = Flask(__name__)

    # Users Blueprint
    from app.users.views import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    # Products Blueprint
    from app.products.views import products_bp
    app.register_blueprint(products_bp, url_prefix="/products")

    # Головна сторінка
    @app.route('/')
    def index():
        return '<h1>Головна сторінка</h1><p><a href="/users/hi/John?age=30">Перейдіть на /users/hi/John</a></p>'

    return app
