from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from alembic import context
from app.models.user_model import Base  # adjust "myapp.models" to the actual location of your Base


# Alembic Config object provides access to values from the .ini file
config = context.config

# Configure logging if a configuration file is provided
if config.config_file_name:
    fileConfig(config.config_file_name)

# Use your model's MetaData object for autogenerate support
target_metadata = Base.metadata


async def run_migrations_online():
    """
    Handle running migrations in 'online' mode with asynchronous database connections.
    """
    # Fetch database URL from the Alembic configuration
    database_url = config.get_main_option("sqlalchemy.url")
    
    # Ensure database URL exists to avoid unexpected failures
    if not database_url:
        raise ValueError("Database URL not defined in Alembic configuration.")
    
    # Create the asynchronous database engine
    async_engine: AsyncEngine = create_async_engine(database_url)

    async with async_engine.begin() as connection:
        # Configure Alembic context with the connection and metadata
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        # Run migrations
        await context.run_migrations()


def run_migrations_offline():
    """
    Handle running migrations in offline mode without establishing async connections.
    """
    # Fetch database URL
    url = config.get_main_option("sqlalchemy.url")
    
    # Configure context in offline mode
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Run the migrations in an offline transaction
    with context.begin_transaction():
        context.run_migrations()


# Determine mode (offline or online) and execute the respective migration logic
if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
