from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp

class ContactForm(FlaskForm):
    name = StringField('Ім\'я', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=4, max=50)])
    phone = StringField('Телефон', validators=[DataRequired(), Regexp(r'^\+380\d{9}$', message="Формат: +380XXXXXXXXX")])
    subject = SelectField('Тема', choices=[('Запитання','Запитання'), ('Пропозиція','Пропозиція'), ('Інше','Інше')], validators=[DataRequired()])
    message = TextAreaField('Повідомлення', validators=[DataRequired(), Length(max=500)])
