from fastapi import FastAPI

from src.api.v1 import api_router
from src.core.config import config
from src.core.logging import setup_logging
from src.db.schema import Base, engine

setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

app.add_api_route("/health", lambda: {"status": "ok"}, methods=["GET"])
app.include_router(api_router, prefix="/api/v1")