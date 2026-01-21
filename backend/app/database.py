from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Force SQLite by default (safe for Render + local dev)
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Use Postgres only if Render provides DATABASE_URL
    engine = create_engine(DATABASE_URL)
else:
    # Fallback to SQLite (works everywhere)
    engine = create_engine(
        "sqlite:///./clariscan.db",
        connect_args={"check_same_thread": False},
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
