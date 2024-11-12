from __future__ import with_statement

import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

# File env.py là file cấu hình quan trọng cho database migrations, sử dụng Alembic (công cụ migrations cho SQLAlchemy)
# Nó giúp quản lý việc thay đổi cấu trúc database một cách có tổ chức và an toàn
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use. => khoi tao cau hinh alembic
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.

# Thiết lập logging để theo dõi quá trình migration. nó sẽ vào file alembic.ini để lấy config được ghi trong đó. sau đó tạo logger với namespace là alembic.env
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

#---------- Cấu hình kết nối database: -----------
# Lấy URL kết nối database từ Flask app
# Thiết lập metadata cho migrations
# 'sqlalchemy.url' là key mặc định được quy định bởi SQLAlchemy và Alembic
# SQLAlchemy sẽ tìm kiếm key này để lấy thông tin kết nối database

# current_app.extensions['migrate']  # Truy cập instance của Flask-Migrate
# current_app.extensions['migrate'].db  # Truy cập SQLAlchemy instance
# current_app.extensions['migrate'].db.engine  # Truy cập database engine
# current_app.extensions['migrate'].db.engine.url  # Lấy URL kết nối. URL kết nối được lấy từ cấu hình của ứng dụng Flask của bạn. Nó được định nghĩa thông qua SQLALCHEMY_DATABASE_URI trong config của Flask app. cụ thể là ở quá trình setup database ở file init.py của shop folder.

# [alembic] sqlalchemy.url = sqlite:///shop.db
# metadata được định nghĩa thông qua các models.py và nó như container chứa thông tin về cấu trúc database. Alembic sử dụng metadata để: So sánh cấu trúc hiện tại với cấu trúc mới, Phát hiện các thay đổi cần migration.
# có thể xem các class model định nghĩa cấu trúc database ở file models.py
from flask import current_app
config.set_main_option(
    'sqlalchemy.url',
    str(current_app.extensions['migrate'].db.engine.url).replace('%', '%%'))
target_metadata = current_app.extensions['migrate'].db.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    # Chạy migrations mà không cần kết nối trực tiếp đến database
    # Hữu ích khi tạo script migration để chạy sau
    # Chỉ cần URL database là đủ 

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # Chạy migrations trực tiếp với database
    # Có kiểm tra thay đổi schema tự động
    # Tránh tạo migrations không cần thiết khi không có thay đổi
    # Sử dụng connection pool để quản lý kết nối hiệu quả


    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            **current_app.extensions['migrate'].configure_args
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
