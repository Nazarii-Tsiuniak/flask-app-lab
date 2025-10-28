from flask import Blueprint

products_bp = Blueprint('products_bp', __name__, url_prefix='/products')

@products_bp.route('/products')
def products_page():
    return "Сторінка товарів"

@products_bp.route('/product/<int:id>')
def product_detail(id):
    return f"Деталі продукту з ID {id}"
