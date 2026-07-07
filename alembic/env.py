from alembic import context
from sqlalchemy import create_engine
import os
from app.db.database import Base
from app.db import entities  
from app.core.config import DATABASE_URL
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)
target_metadata = Base.metadata
# 1. Load Config


# 2. Load Models for Autogenerate
from app.db.database import Base
target_metadata = Base.metadata

# 3. Get URL from Environment Variables
def get_url():
    return os.getenv("DATABASE_URL", "sqlite:///./app.db")

def run_migrations_offline():
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(get_url())
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

