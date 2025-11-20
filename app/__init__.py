# app/__init__.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager  
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()          


def create_app(config_name="development"):
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)

    from app.config import DevelopmentConfig, TestingConfig, ProductionConfig
    configs = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig
    }
    app.config.from_object(configs.get(config_name, DevelopmentConfig))

    db.init_app(app)
    migrate.init_app(app, db)

    # 🔹 Імпорт моделей після db.init_app
    from app.users.models import User
    from app.posts.models import Post

    # 🔹 Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = "users.login"     # куди ганяти неавторизованих
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.main import main_bp
    from app.products.views import products_bp
    from app.users.views import users_bp
    from app.posts import post_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(post_bp, url_prefix='/posts')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app
