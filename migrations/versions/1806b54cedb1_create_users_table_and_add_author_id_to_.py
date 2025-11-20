"""Create users table and add author_id to posts

Revision ID: 1806b54cedb1
Revises: 58117b304f57
Create Date: 2025-11-20 21:38:14.056784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1806b54cedb1'
down_revision = '58117b304f57'
branch_labels = None
depends_on = None


def upgrade():
    # 1. створюємо таблицю users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=50), nullable=False, unique=True),
        sa.Column("email", sa.String(length=120), nullable=False, unique=True),
        sa.Column("password", sa.String(length=255), nullable=False),
    )

    # 2. додаємо стовпець author_id у posts
    op.add_column(
        "posts",
        sa.Column("author_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_posts_author",
        source_table="posts",
        referent_table="users",
        local_cols=["author_id"],
        remote_cols=["id"],
    )


def downgrade():
    # спочатку прибираємо зв'язок і колонку, потім таблицю users
    op.drop_constraint("fk_posts_author", "posts", type_="foreignkey")
    op.drop_column("posts", "author_id")
    op.drop_table("users")