import uuid
from sqlalchemy import select
import logging

from app.db.postgres.schema import NutritionMetaData, FoodNutrients100g
from app.models.NutritionModel import NutritionCreate

class NutritionRepository:
    def __init__(self, db):
        self.db = db

    def get_or_create(self, data: NutritionCreate) -> NutritionMetaData:
        nutrition = self.db.query(NutritionMetaData).filter_by(
            nutrition=data.nutrition
        ).first()

        if not nutrition:
            nutrition = NutritionMetaData(
                nutrition=data.nutrition,
                nutrition_class=data.nutrition_class
            )
            
            self.db.add(nutrition)
            self.db.flush()

        return nutrition
    
    def get_all(self) -> list[NutritionMetaData]:
        try:
            query = select(NutritionMetaData)
            result = self.db.execute(query).mappings().all()
            
            return result
        except Exception as e:
            logging.error("Internal Server Error:" + e)
    
    def get_nutrients_by_food_ids(self, data: list[uuid.UUID]) -> list:
        try:
            query = select(FoodNutrients100g.food_id, FoodNutrients100g.value, NutritionMetaData.nutrition, NutritionMetaData.nutrition_class)\
                .outerjoin(FoodNutrients100g)\
                .where(FoodNutrients100g.food_id.in_(data))
                
            result = self.db.execute(query).mappings().all()
            
            return result
        except Exception as e:
            logging.error("Internal Server Error:" + e)
            raise e