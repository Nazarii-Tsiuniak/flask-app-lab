# C:\Users\User\flask_app_Tsiuniak\app\main\views.py
from flask import render_template, request, redirect, url_for, flash
from . import main_bp
from .forms import ContactForm
import logging

# Налаштування логування контактних повідомлень
logging.basicConfig(
    filename='contact.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@main_bp.route('/')
def home():
    return render_template('main/resume.html', title="Резюме")

@main_bp.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        # Логування даних форми
        logging.info(
            f"New message from {form.name.data} ({form.email.data}), "
            f"phone: {form.phone.data}, subject: {form.subject.data}, "
            f"message: {form.message.data}"
        )
        # Flash повідомлення про успішну відправку
        flash(f"Повідомлення від {form.name.data} ({form.email.data}) успішно надіслано!", "success")
        return redirect(url_for('main.contacts'))  # Post/Redirect/Get
    elif request.method == 'POST':
        # Flash повідомлення при помилці валідації
        flash("Помилка при відправленні форми. Перевірте дані.", "danger")
    return render_template('main/contacts.html', title="Контакти", form=form)
