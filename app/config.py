import os

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.abspath(os.path.join(basedir, '..', 'instance'))

# Створюємо папку instance, якщо її немає
os.makedirs(instance_path, exist_ok=True)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    db_file = os.path.join(instance_path, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_file}"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProductionConfig(Config):
    db_file = os.path.join(instance_path, 'prod.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_file}"
