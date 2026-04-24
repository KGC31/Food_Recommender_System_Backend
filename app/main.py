from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import config
from app.core.logging import setup_logging
from app.db.postgres.schema import Base, engine
from app.utils.api_response import CustomAPIResponse
from app.core.exceptions import APIException
from fastapi.middleware.cors import CORSMiddleware

setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler for APIException
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return CustomAPIResponse(
        success=False,
        error_code=exc.error_code,
        message=exc.message
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "Unexpected error occurred"
        }
    )

app.add_api_route("/health", lambda: {"status": "ok"}, methods=["GET"])
app.include_router(api_router, prefix="/api/v1")