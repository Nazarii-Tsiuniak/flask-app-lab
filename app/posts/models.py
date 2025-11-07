from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    author = db.Column(db.String(50), default='Anonymous')

    def __repr__(self):
        return f"<Post {self.title}>"

    # --- Повернути активні пости ---
    @classmethod
    def active_posts(cls):
        return cls.query.filter_by(is_active=True).order_by(cls.posted.desc())

    # --- Створення нового поста ---
    @classmethod
    def create(cls, title, content, category=None, author='Anonymous', is_active=True, posted=None):
        post = cls(
            title=title,
            content=content,
            category=category,
            author=author,
            is_active=is_active,
            posted=posted or datetime.utcnow()
        )
        db.session.add(post)
        db.session.commit()
        return post

    # --- Оновлення поста ---
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    # --- Видалення поста ---
    def delete(self):
        db.session.delete(self)
        db.session.commit()
