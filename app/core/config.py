import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from app.core.logging import setup_logging

setup_logging()
load_dotenv()

class Config(BaseSettings):
    PROJECT_NAME: str =  "FoodRecommenderSystem"
    VERSION: str = "1.0.0"
    
    DEBUG: bool = os.getenv("DEBUG").lower() == "true" if os.getenv("DEBUG") else False
    
    # PostgreSQL configuration
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    PGPASSWORD: str = os.getenv("PGPASSWORD")
    PGHOST: str = os.getenv("PGHOST")
    PG_PORT: int = int(os.getenv("PG_PORT")) if os.getenv("PG_PORT") else 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    
    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.PGPASSWORD}@{self.PGHOST}:{self.PG_PORT}/{self.POSTGRES_DB}"
    
config = Config()