from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from .forms import LoginForm

users_bp = Blueprint('users', __name__, template_folder='templates')

# Заглушка користувача
VALID_USER = {'username': 'admin', 'password': '12345'}

# -------------------- LOGIN --------------------
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == VALID_USER['username'] and password == VALID_USER['password']:
            session['user'] = username
            remember_text = "запам'ятати" if form.remember.data else "не запам'ятовувати"
            flash(f'Вхід успішний! ({remember_text})', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Невірний логін або пароль', 'danger')
            return redirect(url_for('users.login'))
    return render_template('login.html', form=form)

# -------------------- PROFILE --------------------
@users_bp.route('/profile')
def profile():
    if 'user' not in session:
        flash('Спершу увійдіть у систему', 'warning')
        return redirect(url_for('users.login'))

    user = session['user']
    cookies = request.cookies  # поточні cookies
    theme = cookies.get('theme', 'light')  # отримуємо тему, якщо немає — світла

    return render_template('profile.html', user=user, cookies=cookies, theme=theme)

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
        # Видалення всіх кукі, окрім session
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
