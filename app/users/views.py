# app/users/views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from app import db, bcrypt
from .models import User
from .forms import LoginForm, RegisterForm, UpdateAccountForm, ChangePasswordForm

users_bp = Blueprint('users', __name__, template_folder='templates')

# -------------------- REGISTER --------------------
@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            image='profile_default.jpg'
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Реєстрація успішна! Тепер можете увійти', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

# -------------------- LOGIN --------------------
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_value = form.username_or_email.data
        user = User.query.filter((User.username == login_value) | (User.email == login_value)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Вхід успішний!', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Невірний логін або пароль', 'danger')
    return render_template('login.html', form=form)

# -------------------- LOGOUT --------------------
@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ви вийшли з системи', 'info')
    return redirect(url_for('users.login'))

# -------------------- ACCOUNT --------------------
@users_bp.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

# -------------------- UPDATE ACCOUNT --------------------
# -------------------- UPDATE ACCOUNT --------------------
@users_bp.route('/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    """Редагування даних користувача та фото профілю"""
    form = UpdateAccountForm()

    if request.method == 'GET':
        # Заповнюємо форму поточними даними користувача
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        # Обробка фото профілю
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(current_app.root_path, 'static/profile_pics', filename)
            form.image.data.save(filepath)
            current_user.image = filename

        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        flash('Профіль оновлено!', 'success')
        return redirect(url_for('users.account'))

    return render_template('update_account.html', user=current_user, form=form)

# -------------------- CHANGE PASSWORD --------------------
@users_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Використовуємо метод check_password() замість доступу до password
        if not current_user.check_password(form.old_password.data):
            flash('Поточний пароль введено невірно!', 'danger')
        else:
            # Для запису нового пароля використовується property password
            current_user.password = form.new_password.data
            db.session.commit()
            flash('Пароль успішно змінено!', 'success')
            return redirect(url_for('users.account'))
    return render_template('change_password.html', form=form)

# -------------------- CHANGE THEME --------------------
@users_bp.route('/theme/<string:theme>')
@login_required
def change_theme(theme):
    if theme not in ['light', 'dark']:
        flash('Невідома тема', 'warning')
        return redirect(url_for('users.account'))

    resp = make_response(redirect(url_for('users.account')))
    resp.set_cookie('theme', theme)
    flash(f'Тема змінена на "{theme}"', 'success')
    return resp
