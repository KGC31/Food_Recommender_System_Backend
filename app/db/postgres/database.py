from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import config

class Base(DeclarativeBase): 
    pass

engine = create_engine(
    config.db_url, 
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine, 
    autocommit=False, 
    autoflush=False
)

metadata = MetaData()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()