from flask import render_template
from . import main_bp

@main_bp.route('/')
def home():
    return render_template('main/resume.html', title="Резюме")

@main_bp.route('/contacts')
def contacts():
    return render_template('main/contacts.html', title="Контакти")
