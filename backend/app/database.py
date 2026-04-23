"""
Database setup: engine, session factory, and declarative Base.

This file is the bridge between Python objects and the actual SQLite file.
Every other part of the app that needs to talk to the DB imports from here.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

# SQLite stores the whole DB in a single file next to the project.
# In production you'd swap this for Postgres/MySQL — only this string changes.
DATABASE_URL = "sqlite:///./school.db"

# The engine is the low-level connection pool to the DB.
# check_same_thread=False is SQLite-specific; other DBs don't need it.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# A SessionLocal is a "conversation" with the DB. Each request opens one,
# uses it, then closes it — so requests don't step on each other.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Parent class for every ORM model. SQLAlchemy uses it to track tables."""
    pass


def get_db():
    """
    FastAPI dependency: yields a DB session for one request, then closes it.
    Routes declare `db: Session = Depends(get_db)` to receive one.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
