from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging

from app.db.postgres.database import get_db
from app.services.FoodService import FoodService
from app.services.RecommenderService import RecommenderService
from app.models.FoodModel import FoodCreate, FoodRecommendationRequest
from app.utils.api_response import CustomAPIResponse
from app.core.error_codes import ErrorCode

router = APIRouter()

@router.post("/create", response_model=CustomAPIResponse)
def create_food(food: FoodCreate, db: Session = Depends(get_db)):
    food_service = FoodService(db)

    try:
        food_service.create_food(food)

        return CustomAPIResponse(
            success=True,
            message="Food created successfully"
        )

    except Exception as e:
        logging.exception(e)
        return CustomAPIResponse(
            success=False,
            error_code=ErrorCode.FOOD_CREATION_FAILED,
            message=f"Failed to create food: {food.food_metadata.name_en}"
        )

@router.get("/search")
def search_foods(query: str, limit: int = 0, db: Session = Depends(get_db)):
    food_service = FoodService(db)
    return food_service.get_food_by_query(query, limit)

@router.get("/{food_id}")
def get_food_by_id(food_id: str, db: Session = Depends(get_db)):
    food_service = FoodService(db)
    return food_service.get_food_by_id(food_id)

@router.post("/recommend")
def recommend_foods(user_metrics: FoodRecommendationRequest, db: Session = Depends(get_db)):
    recommender_service = RecommenderService(db)
    
    try:
        return recommender_service.get_recommended_foods(user_metrics)
    
    except Exception as e:
        logging.exception(e)
        return CustomAPIResponse(
            success=False,
            error_code=ErrorCode.FOOD_RECOMMENDATION_FAILED,
            message="Failed to get food recommendations"
        )