import uuid
from alchemy.orm import Session
from src.db.schema import FoodMetadata, NutritionMetaData, FoodNutrients

class FoodService():
    def __init__(self, db: Session):
        self.db = db
        
    def get_food_by_name(self, name: str):
        return self.db.query(FoodMetadata).filter(FoodMetadata.name == name).first()
        
    def get_food_by_id(self, food_id: uuid.UUID):
        return self.db.query(FoodMetadata).filter(FoodMetadata.id == food_id).first()
    
    def get_food_by_query(self, query: str, limit: int = 0):
        if limit > 0:
            return self.db.query(FoodMetadata).filter(FoodMetadata.name.ilike(f"%{query}%")).limit(limit).all()
        else:
            return self.db.query(FoodMetadata).filter(FoodMetadata.name.ilike(f"%{query}%")).all()
    
    def get_nutrition_by_food_id(self, food_id: uuid.UUID):
        return (
            self.db.query(NutritionMetaData.nutrition, FoodNutrients.value)
            .join(FoodNutrients, NutritionMetaData.id == FoodNutrients.nutrition_id)
            .filter(FoodNutrients.food_id == food_id)
            .all()
        )
    