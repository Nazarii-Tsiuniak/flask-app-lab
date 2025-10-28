from flask import Blueprint, render_template

products_bp = Blueprint('products', __name__, template_folder='templates')

# Дані проєктів
projects = [
    {
        "id": 1,
        "name": "Портфоліо сайт",
        "description": "Сайт для демонстрації моїх робіт та резюме.",
        "tech": ["Flask", "HTML", "CSS", "Bootstrap"],
        "status": "В процесі",
        "date": "2025-10-01",
        "links": {"GitHub": "https://github.com/user/portfolio"},
        "content": "Цей сайт включає сторінки резюме, проєктів, контактів та профілю користувача. Підтримує світлу та темну тему."
    },
    {
        "id": 2,
        "name": "Калькулятор депозитів",
        "description": "Python-додаток для розрахунку депозитів з помісячною деталізацією.",
        "tech": ["Python"],
        "status": "Завершено",
        "date": "2025-09-15",
        "links": {"GitHub": "https://github.com/user/deposit-calculator"},
        "content": "Консольний калькулятор з графіком, розбивкою по місяцях та сумарним доходом."
    },
    {
        "id": 3,
        "name": "3D сцена OpenGL",
        "description": "Візуалізація 3D примітивів з анімацією.",
        "tech": ["Python", "OpenGL"],
        "status": "Завершено",
        "date": "2025-09-20",
        "links": {"GitHub": "https://github.com/user/opengl-3d"},
        "content": "Сцена демонструє обертові сфери, куби та циліндри з використанням бібліотеки GLUT та GLU."
    }
]

@products_bp.route('/products')
def products():
    return render_template('products/products.html', projects=projects)

@products_bp.route('/products/<int:id>')
def detail_post(id):
    project = next((p for p in projects if p["id"] == id), None)
    if project:
        return render_template('products/product_detail.html', project=project)
    return "Проєкт не знайдено", 404
