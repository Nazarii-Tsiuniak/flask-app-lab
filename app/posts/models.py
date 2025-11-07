from datetime import datetime
from app import db
from sqlalchemy import Enum

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Додано 'General' до Enum
    category = db.Column(
        Enum('news', 'publication', 'tech', 'other', 'General', name='post_category'),
        nullable=False,
        default='General'
    )
