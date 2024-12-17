
import asyncio
from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.engine import Connection
from sqlalchemy import pool


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
=======
# Replace with your actual database URL
config = context.config
target_metadata = None  # Import your metadata if needed

async def run_migrations_online():
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

asyncio.run(run_migrations_online())

