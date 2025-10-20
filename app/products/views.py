from flask import Blueprint

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/')
def products_index():
    return "<h1>Products Home</h1><p>Список продуктів буде тут.</p>"

@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    return f"<h1>Product {product_id}</h1><p>Деталі продукту {product_id}.</p>"
