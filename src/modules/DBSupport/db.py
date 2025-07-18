"""db.py

Database engine and async session setup for use with SQLAlchemy 2.x and async.
"""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Async-compatible SQLite URL
DATABASE_URL = "sqlite+aiosqlite:///./instance/app.db"

# Create the asynchronous engine
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)

# Create an async sessionmaker
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Declarative base class for models
class Base(DeclarativeBase):
    pass
