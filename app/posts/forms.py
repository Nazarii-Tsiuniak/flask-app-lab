from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.fields import DateTimeLocalField  # новий правильний імпорт
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    content = TextAreaField('Content', validators=[DataRequired()])
    
    # Випадаючий вибір дати та часу
    publish_date = DateTimeLocalField(
        'Publish Date', 
        format='%Y-%m-%dT%H:%M',  # формат для datetime-local
        default=None
    )

    enabled = BooleanField('Enabled', default=True)

    category = SelectField(
        'Category',
        choices=[('news', 'News'), ('publication', 'Publication'), ('tech', 'Tech'), ('other', 'Other'), ('General', 'General')],
        default='General'
    )

    submit = SubmitField('Submit')
