from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from .forms import LoginForm, RegisterForm
from app.users.models import User
from app import db
from flask_login import login_user, logout_user, login_required, current_user

users_bp = Blueprint('users', __name__, template_folder='templates')

# -------------------- LOGIN --------------------
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_value = form.username_or_email.data
        password = form.password.data

        # шукаємо користувача за username або email
        user = User.query.filter((User.username==login_value) | (User.email==login_value)).first()

        if user and user.password == password:
            login_user(user, remember=form.remember.data)
            flash('Вхід успішний!', 'success')
            return redirect(url_for('users.profile'))

        else:
            flash('Невірний логін або пароль', 'danger')
            return redirect(url_for('users.login'))

    return render_template('login.html', form=form)

# -------------------- REGISTER --------------------
@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username==form.username.data) | (User.email==form.email.data)).first()
        if existing_user:
            flash('Користувач з таким username або email вже існує', 'warning')
            return redirect(url_for('users.register'))

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Реєстрація успішна! Тепер можете увійти', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)

# -------------------- PROFILE --------------------
# -------------------- PROFILE --------------------
@users_bp.route('/profile')
@login_required
def profile():
    user = current_user
    theme = request.cookies.get('theme', 'light')
    cookies = request.cookies.to_dict()
    return render_template('profile.html', user=user, theme=theme, cookies=cookies)

# -------------------- LOGOUT --------------------
@users_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Ви вийшли з системи', 'info')
    return redirect(url_for('users.login'))

# -------------------- SET COOKIE --------------------
@users_bp.route('/profile/set_cookie', methods=['POST'])
def set_cookie():
    if 'user' not in session:
        flash('Спершу увійдіть у систему', 'warning')
        return redirect(url_for('users.login'))

    key = request.form.get('key')
    value = request.form.get('value')
    resp = make_response(redirect(url_for('users.profile')))
    if key and value:
        resp.set_cookie(key, value)
        flash(f'Кукі "{key}" встановлено', 'success')
    else:
        flash('Вкажіть ключ та значення', 'warning')
    return resp

# -------------------- DELETE COOKIE --------------------
@users_bp.route('/profile/delete_cookie', methods=['POST'])
def delete_cookie():
    if 'user' not in session:
        flash('Спершу увійдіть у систему', 'warning')
        return redirect(url_for('users.login'))

    key = request.form.get('key')
    resp = make_response(redirect(url_for('users.profile')))
    if key:
        resp.delete_cookie(key)
        flash(f'Кукі "{key}" видалено', 'info')
    else:
        for cookie_key in request.cookies.keys():
            if cookie_key != 'session':
                resp.delete_cookie(cookie_key)
        flash('Всі кукі видалено', 'info')
    return resp

# -------------------- CHANGE THEME --------------------
@users_bp.route('/profile/theme/<string:theme>')
def change_theme(theme):
    if 'user' not in session:
        flash('Спершу увійдіть у систему', 'warning')
        return redirect(url_for('users.login'))

    if theme not in ['light', 'dark']:
        flash('Невідома тема', 'warning')
        return redirect(url_for('users.profile'))

    resp = make_response(redirect(url_for('users.profile')))
    resp.set_cookie('theme', theme)
    flash(f'Тема змінена на "{theme}"', 'success')
    return resp
