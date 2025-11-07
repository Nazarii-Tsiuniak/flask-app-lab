from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[('publication', 'Publication'), ('other', 'Other')])
    publish_date = DateTimeField('Publish Date', default=datetime.utcnow)
    enabled = BooleanField('Enabled', default=True)
    submit = SubmitField('Save')
