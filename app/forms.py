# C:\Users\User\flask_app_Tsiuniak\app\forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp

# -------------------- LOGIN FORM --------------------
class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(message="Обов'язкове поле")]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Обов'язкове поле"),
            Length(min=4, max=10, message="Мінімум 4, максимум 10 символів")
        ]
    )
    remember = BooleanField('Remember me')

# -------------------- CONTACT FORM --------------------
class ContactForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(message="Обов'язкове поле")]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Обов'язкове поле"),
            Email(message="Невірний email"),
            Length(min=4, max=100)
        ]
    )
    phone = StringField(
        'Phone',
        validators=[
            DataRequired(message="Обов'язкове поле"),
            Regexp(r'^\+380\d{9}$', message="Формат: +380XXXXXXXXX")
        ]
    )
    subject = SelectField(
        'Subject',
        choices=[
            ('general', 'Загальне питання'),
            ('support', 'Підтримка'),
            ('feedback', 'Відгук')
        ],
        validators=[DataRequired(message="Обов'язкове поле")]
    )
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message="Обов'язкове поле"),
            Length(max=500, message="Максимум 500 символів")
        ]
    )
