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
        
@router.get("/{food_id}")
def get_food_by_id(food_id: str, db: Session = Depends(get_db)):
    try:
        food_service = FoodService(db)
        food_data = food_service.get_food_by_id(food_id)

        if not food_data:
            return CustomAPIResponse(
                success=False,
                error_code=ErrorCode.FOOD_NOT_FOUND,
                message=f"Food with id {food_id} not found"
            )

        return CustomAPIResponse(
            data=food_data,
            success=True,
            message="Food retrieve successfully"
        )
    except Exception as e:
        logging.exception(e)
        return CustomAPIResponse(
            success=False,
            error_code=ErrorCode.FOOD_RETRIEVAL_FAILED,
            message=f"Failed to retrieve food with id {food_id}"
        )

@router.put("/{food_id}")
def update_food(food_id: str, food: FoodCreate, db: Session = Depends(get_db)):
    food_service = FoodService(db)

    try:
        success = food_service.update_food_by_id(food_id, food)

        if not success:
            return CustomAPIResponse(
                success=False,
                error_code=ErrorCode.FOOD_NOT_FOUND,
                message=f"Food with id {food_id} not found"
            )

        return CustomAPIResponse(
            success=True,
            message=f"Food with id {food_id} updated successfully"
        )

    except Exception as e:
        logging.exception(e)
        return CustomAPIResponse(
            success=False,
            error_code=ErrorCode.FOOD_UPDATE_FAILED,
            message=f"Failed to update food with id {food_id}"
        )
    
@router.delete("/{food_id}", response_model=CustomAPIResponse)
def delete_food(food_id: str, db: Session = Depends(get_db)):
    food_service = FoodService(db)

    try:
        success = food_service.delete_food_by_id(food_id)

        if not success:
            return CustomAPIResponse(
                success=False,
                error_code=ErrorCode.FOOD_NOT_FOUND,
                message=f"Food with id {food_id} not found"
            )

        return CustomAPIResponse(
            success=True,
            message=f"Food with id {food_id} deleted successfully"
        )

    except Exception as e:
        logging.exception(e)
        return CustomAPIResponse(
            success=False,
            error_code=ErrorCode.FOOD_DELETION_FAILED,
            message=f"Failed to delete food with id {food_id}"
        )

@router.post("/recommend")
def recommend_foods(user_metrics: FoodRecommendationRequest, db: Session = Depends(get_db)):
    recommender_service = RecommenderService(db)
    
    try:
        recommend_data = recommender_service.get_recommended_foods(user_metrics)
        
        return CustomAPIResponse(
            data=recommend_data,
            success=True,
            message="Retrieve food recommendation successfully"
        )
    
    except Exception as e:
        logging.exception(e)
        return CustomAPIResponse(
            success=False,
            error_code=ErrorCode.FOOD_RECOMMENDATION_FAILED,
            message="Failed to get food recommendations"
        )