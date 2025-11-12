"""Insert data into products table

Revision ID: 6361ff5728a4
Revises: 7844f910a546
Create Date: 2025-11-12 19:49:21.026405
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Float, Boolean, Integer

# revision identifiers, used by Alembic.
revision = '6361ff5728a4'
down_revision = '7844f910a546'
branch_labels = None
depends_on = None

# Тимчасові об'єкти таблиць
categories_table = table('categories',
    column('id', Integer),
    column('name', String)
)

products_table = table('products',
    column('name', String),
    column('price', Float),
    column('active', Boolean),
    column('category_id', Integer)
)

def upgrade():
    # --- Описи таблиць для bulk_insert ---
    categories_table = table('categories', column('name', sa.String))

    products_table = table('products',
        column('name', sa.String),
        column('price', sa.Float),
        column('active', sa.Boolean),
        column('category_id', sa.Integer),
    )

    # --- Вставка категорій (ігноруємо дублікати) ---
    op.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Electronics')")
    op.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Books')")
    op.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Clothing')")

    # Отримуємо id категорій
    conn = op.get_bind()
    electronics_id = conn.execute(sa.text("SELECT id FROM categories WHERE name='Electronics'")).scalar()
    books_id = conn.execute(sa.text("SELECT id FROM categories WHERE name='Books'")).scalar()
    clothing_id = conn.execute(sa.text("SELECT id FROM categories WHERE name='Clothing'")).scalar()

    # --- Вставка продуктів ---
    op.execute(sa.text("""
        INSERT OR IGNORE INTO products (name, price, active, category_id)
        VALUES ('Laptop', 1200.0, 1, :electronics_id)
    """).bindparams(electronics_id=electronics_id))

    op.execute(sa.text("""
        INSERT OR IGNORE INTO products (name, price, active, category_id)
        VALUES ('Smartphone LG', 800.0, 1, :electronics_id)
    """).bindparams(electronics_id=electronics_id))

    op.execute(sa.text("""
        INSERT OR IGNORE INTO products (name, price, active, category_id)
        VALUES ('Novel', 20.0, 1, :books_id)
    """).bindparams(books_id=books_id))

    op.execute(sa.text("""
        INSERT OR IGNORE INTO products (name, price, active, category_id)
        VALUES ('T-Shirt', 25.0, 0, :clothing_id)
    """).bindparams(clothing_id=clothing_id))


def downgrade():
    op.execute("""
        DELETE FROM products
        WHERE name IN ('Laptop', 'Smartphone LG', 'Novel', 'T-Shirt')
    """)
    op.execute("""
        DELETE FROM categories
        WHERE name IN ('Electronics', 'Books', 'Clothing')
    """)
