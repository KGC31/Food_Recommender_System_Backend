from fastapi import APIRouter

from app.api.v1 import FoodRouter

api_router = APIRouter()

api_router.include_router(FoodRouter.router, prefix="/foods", tags=["Foods"])
# api_router.include_router(nutrition.router, prefix="/nutrition", tags=["Nutrition"])