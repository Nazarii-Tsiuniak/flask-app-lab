"""Add users password_hash column / users model

Revision ID: a928cce728ae
Revises: 9238f075708f
Create Date: 2025-11-28 20:45:09.008201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a928cce728ae'
down_revision = '9238f075708f'
branch_labels = None
depends_on = None


def upgrade():
    # додаємо нову колонку password_hash до таблиці users
    op.add_column(
        'users',
        sa.Column('password_hash', sa.String(length=128), nullable=True)
    )

    # якщо хочеш зробити NOT NULL, треба або:
    # 1) спершу заповнити значення по замовчуванню через окремий скрипт,
    # 2) або задати server_default, а потім прибрати його.
    # Простий варіант (опціонально, якщо потрібен дефолт):
    # op.alter_column('users', 'password_hash', nullable=False)


def downgrade():
    # видаляємо колонку при відкаті
    op.drop_column('users', 'password_hash')
