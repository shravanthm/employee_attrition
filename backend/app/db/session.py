"""Database session management with graceful PostgreSQL check and SQLite fallback."""

import logging
import os
from collections.abc import Generator

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

logger = logging.getLogger(__name__)

Base = declarative_base()


def get_engine(db_url: str = None):
    url = db_url or settings.DATABASE_URL
    try:
        # Test if PostgreSQL is reachable if postgresql in url
        if "postgresql" in url:
            test_engine = create_engine(url, connect_args={"connect_timeout": 3})
            with test_engine.connect() as conn:
                pass
            logger.info("Connected to PostgreSQL successfully.")
            return create_engine(url, pool_pre_ping=True)
    except Exception as e:
        logger.warning(
            f"PostgreSQL connection to {url} failed: {e}. Falling back to SQLite for local development."
        )
        os.makedirs("data", exist_ok=True)
        fallback_url = settings.SQLITE_FALLBACK_URL
        return create_engine(
            fallback_url,
            connect_args={"check_same_thread": False}
        )

    # Direct sqlite connection if configured
    connect_args = {"check_same_thread": False} if "sqlite" in url else {}
    return create_engine(url, connect_args=connect_args)


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
