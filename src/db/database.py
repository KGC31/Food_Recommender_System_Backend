from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.core.config import config

class Base(DeclarativeBase): 
    pass

engine = create_engine(config.db_url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
metadata = MetaData()