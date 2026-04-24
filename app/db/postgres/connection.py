from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import config

database_url = config.db_url

engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()