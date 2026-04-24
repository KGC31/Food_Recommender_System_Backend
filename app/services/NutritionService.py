import uuid

# Repositories
from app.repositories.NutritionRepository import NutritionRepository

# Schemas
from app.db.postgres.schema import NutritionMetaData

class NutritionService:
    def __init__(self, db):
        self.db = db
        self.nutrition_repository = NutritionRepository(db)
        
    def get_all_nutrients(self) -> list:
        result = self.nutrition_repository.get_all()
        
        return result
    
    def get_nutrients_by_food_ids(self, data: list[uuid.UUID]) -> list[NutritionMetaData]:
        result = self.nutrition_repository.get_nutrients_by_food_ids(data)
        
        return result