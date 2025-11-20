from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired
from .models import Tag
from app.users.models import User  # <-- імпорт моделі User

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Контент', validators=[DataRequired()])
    category = SelectField('Категорія', choices=[('News','News'), ('Blog','Blog'), ('Tutorial','Tutorial')])
    author_id = SelectField('Автор', coerce=int)  # поле вибору автора
    tags = SelectMultipleField('Теги', coerce=int)
    enabled = BooleanField('Активний')
    publish_date = DateField('Дата публікації', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Зберегти')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
        self.author_id.choices = [(user.id, user.username) for user in User.query.all()]
