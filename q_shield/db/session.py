import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from q_shield.db.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./q_shield.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initializes schema tables in the target database."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """FastAPI dependency for database session management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
