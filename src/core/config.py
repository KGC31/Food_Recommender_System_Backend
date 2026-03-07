import os
import logging
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from src.core.logging import setup_logging

setup_logging()
load_dotenv()

class Config(BaseSettings):
    PROJECT_NAME: str =  "FoodRecommenderSystem"
    VERSION: str = "1.0.0"
    
    DEBUG: bool = os.getenv("DEBUG").lower() == "true" if os.getenv("DEBUG") else False
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT")) if os.getenv("DB_PORT") else 5432
    DB_NAME: str = os.getenv("DB_NAME")

    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
config = Config()