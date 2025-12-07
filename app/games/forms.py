# app/games/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from flask_wtf.file import FileAllowed
from app.games.models import Genre

class GameForm(FlaskForm):
    title = StringField("Назва", validators=[DataRequired(), Length(min=2, max=120)])
    description = TextAreaField("Опис", validators=[Optional(), Length(max=2000)])
    price = FloatField("Ціна (UAH)", validators=[Optional(), NumberRange(min=0)], default=0.0)
    genre = SelectField("Жанр", coerce=int, validators=[DataRequired()])
    image = FileField("Зображення (jpg/png/jpeg)", validators=[Optional(), FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField("Зберегти")

    def set_genre_choices(self):
        # підтягує жанри з БД
        self.genre.choices = [(g.id, g.name) for g in Genre.query.order_by(Genre.name).all()]

class DeleteGameForm(FlaskForm):
    submit = SubmitField("Видалити")
