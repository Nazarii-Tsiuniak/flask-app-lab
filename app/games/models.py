# app/games/models.py
from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.users.models import User

class Genre(db.Model):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(db.Text, nullable=True)

    games: Mapped[list["Game"]] = relationship("Game", back_populates="genre", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Genre {self.name}>"

class Game(db.Model):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(120), nullable=False)
    description: Mapped[str] = mapped_column(db.Text, nullable=True)
    price: Mapped[float] = mapped_column(db.Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)

    # foreign keys
    genre_id: Mapped[int] = mapped_column(db.ForeignKey("genres.id"), nullable=False)
    owner_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)

    # relationships
    genre: Mapped["Genre"] = relationship("Genre", back_populates="games")
    owner: Mapped["User"] = relationship("app.users.models.User", backref="games")

    image_filename: Mapped[str] = mapped_column(db.String(255), nullable=True)  # optional

    def __repr__(self):
        return f"<Game {self.title}>"
