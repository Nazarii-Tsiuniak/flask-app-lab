# app/users/models.py
from app import db, bcrypt
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.posts.models import Post

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)
    
    image: Mapped[str] = mapped_column(db.String(255), nullable=True, default='profile_default.jpg')
    about_me: Mapped[str] = mapped_column(db.Text, nullable=True)
    last_seen: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)

    posts: Mapped[list["Post"]] = relationship(
        "Post", back_populates="author", cascade="all, delete-orphan"
    )

    # write-only password property
    @property
    def password(self):
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, plain_password: str):
        if not plain_password:
            raise ValueError("Password cannot be empty")
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    # метод перевірки пароля
    def check_password(self, plain_password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, plain_password)

    # get_id для Flask-Login
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User {self.username}>"
