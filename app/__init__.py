from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
import os

# 🔹 Додаємо єдиний стиль іменування обмежень
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

# 🔹 Базовий клас для моделей
class Base(DeclarativeBase):
    metadata = metadata

# 🔹 Ініціалізація розширень
db = SQLAlchemy(model_class=Base)
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

    # 🔹 Імпорт моделей після ініціалізації db
    from app.products.models import Product
    from app.products.models import Category  # тепер уже можна

    # 🔹 Реєстрація блюпринтів
    from app.main import main_bp
    from app.products.views import products_bp
    from app.users.views import users_bp

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix="/products")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app
