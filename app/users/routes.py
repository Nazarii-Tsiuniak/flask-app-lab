from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response

users_bp = Blueprint('users', __name__, template_folder='templates')

VALID_USERNAME = "Nazarii"
VALID_PASSWORD = "1234"

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['user'] = username
            flash(f'Вхід успішний! Вітаємо, {username}', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Невірне ім’я користувача або пароль!', 'danger')
            return redirect(url_for('users.login'))
    return render_template('users/login.html')


@users_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        flash('Будь ласка, увійдіть у систему!', 'warning')
        return redirect(url_for('users.login'))

    username = session['user']
    cookies = request.cookies
    color_scheme = cookies.get('color_scheme', 'light')

    if request.method == 'POST':
        key = request.form.get('key')
        value = request.form.get('value')
        expires = request.form.get('expires', type=int)
        action = request.form.get('action')

        resp = make_response(redirect(url_for('users.profile')))

        if action == 'add' and key and value:
            resp.set_cookie(key, value, max_age=expires if expires else None)
            flash(f'Кукі "{key}" успішно додано!', 'success')
            return resp
        elif action == 'delete_all':
            for k in cookies.keys():
                resp.delete_cookie(k)
            flash('Всі кукі видалено.', 'info')
            return resp
        elif action == 'delete_one' and key:
            resp.delete_cookie(key)
            flash(f'Кукі "{key}" видалено.', 'info')
            return resp

    return render_template('users/profile.html', username=username, cookies=cookies, color_scheme=color_scheme)


@users_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))


@users_bp.route('/set_color/<scheme>')
def set_color(scheme):
    if 'user' not in session:
        flash('Спочатку увійдіть у систему.', 'warning')
        return redirect(url_for('users.login'))
    resp = make_response(redirect(url_for('users.profile')))
    resp.set_cookie('color_scheme', scheme, max_age=60*60*24*30)
    flash(f'Колірна схема змінена на {scheme}.', 'success')
    return resp
