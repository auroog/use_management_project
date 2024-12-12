from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from alembic import context
from app.models.user_model import Base  # adjust "myapp.models" to the actual location of your Base


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

async def run_migrations_online():
    """Run migrations in 'online' mode with async connection."""
    # Fetch database URL from your Alembic configuration
    database_url = config.get_main_option("sqlalchemy.url")
    # Create the async engine
    async_engine: AsyncEngine = create_async_engine(database_url)

    async with async_engine.begin() as connection:
        # Configure Alembic context with the connection
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        # Run migrations
        await context.run_migrations()


# Handle migration modes
if context.is_offline_mode():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    import asyncio
    asyncio.run(run_migrations_online())
