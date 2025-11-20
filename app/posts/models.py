from app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

# --- Асоціативна таблиця для Many-to-Many ---
post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship("User", back_populates="posts")

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=post_tags,
        back_populates="posts"
    )

    def __repr__(self):
        return f"<Post {self.title}>"

class Tag(db.Model):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        secondary=post_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"
