from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"

    # Імпорт і реєстрація блюпринтів
    from .main.views import main_bp
    from .users.views import users_bp
    from .products.views import products_bp

    app.register_blueprint(main_bp)  # Без url_prefix, бо '/' використовується
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(products_bp, url_prefix='/products')

    return app
