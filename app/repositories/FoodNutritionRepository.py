from app.db.neo4j.connection import neo4j_conn
from app.db.postgres.connection import get_db

from app.db.postgres.schema import FoodNutrients100g
from app.models.FoodNutritionModel import FoodNutritionCreate

class FoodNutritionRepository:
    def __init__(self, db):
        self.db = db

    def create(self, data: FoodNutritionCreate) -> FoodNutrients100g:
        food_nutrition = FoodNutrients100g(
            food_id=data.food_id,
            nutrition_id=data.nutrition_id,
            value=data.value
        )
        
        self.db.add(food_nutrition)
        self.db.flush()
        
        return food_nutrition