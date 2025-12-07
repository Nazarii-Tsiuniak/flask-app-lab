from __future__ import with_statement
from logging.config import fileConfig
import logging

from alembic import context
from sqlalchemy import engine_from_config, pool
from flask import current_app

# Конфігурація Alembic
config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Доступ до метаданих моделей
target_metadata = current_app.extensions['migrate'].db.metadata

# ІМПОРТУЄМО ВСІ МОДЕЛІ щоб Alembic їх бачив
from app.users.models import User
from app.posts.models import Post
from app.games.models import Game, Genre # <--- додано
# Якщо додаси нові моделі — просто імпортуй сюди

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = current_app.config.get("SQLALCHEMY_DATABASE_URI")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=current_app.config.get("SQLALCHEMY_DATABASE_URI"))

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


# запуск
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
