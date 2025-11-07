from flask import Blueprint

post_bp = Blueprint(
    'post_bp',
    __name__,
    template_folder='templates',
    static_folder='static',  # папка всередині блюпринта
    static_url_path='/posts/static'  # URL для доступу до статичних файлів
)

from . import views
