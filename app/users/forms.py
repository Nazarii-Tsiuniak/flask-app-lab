# app/users/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from flask_login import current_user
from app.users.models import User

# -------------------- REGISTER FORM --------------------
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50)])
    confirm_password = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

# -------------------- LOGIN FORM --------------------
class LoginForm(FlaskForm):
    username_or_email = StringField('Username або Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50)])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField('Login')

# -------------------- UPDATE ACCOUNT FORM --------------------
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('Про себе', validators=[Length(max=500)])
    image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, field):
        if field.data != current_user.username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already in use.')

    def validate_email(self, field):
        if field.data != current_user.email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Email already registered.')

# -------------------- CHANGE PASSWORD FORM --------------------
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=4, max=50)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')
