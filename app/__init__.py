from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name="development"):
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)

    # Вибір конфігурації
    from app.config import DevelopmentConfig, TestingConfig, ProductionConfig
    configs = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig
    }
    app.config.from_object(configs.get(config_name, DevelopmentConfig))

    # Ініціалізація розширень
    db.init_app(app)
    migrate.init_app(app, db)

    # --- 🔹 Реєстрація блюпринтів ---
    from app.main import main_bp
    from app.products.views import products_bp
    from app.users.views import users_bp
    from app.posts import post_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(main_bp)  # головна сторінка '/'
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(post_bp, url_prefix='/posts')

    # --- Обробник помилки 404 ---
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app
