"""
Database engine.
SQLite is configured for WAL (Write-Ahead Logging) mode, which lets many
concurrent readers proceed while a single writer is active:
the classic "database is locked" error mostly comes from the default
rollback-journal mode, not from SQLite itself.
"""

from app.config import get_settings
from collections.abc import AsyncGenerator
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)


@event.listens_for(engine.sync_engine, "connect")
def _set_sqlite_pragma(dbapi_connection) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")  # concurrent reads during writes
    cursor.execute(
        "PRAGMA synchronous=NORMAL"
    )  # good durability/speed tradeoff with WAL
    cursor.execute(
        "PRAGMA busy_timeout=30000"
    )  # wait up to 30s instead of erroring immediately
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: yields a DB session and guarantees it is closed."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_models() -> None:
    """
    Create tables if they don't exist yet.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
