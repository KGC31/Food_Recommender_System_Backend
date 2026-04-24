import uuid
from pydantic import BaseModel

class FoodNutritionBaseModel(BaseModel):
    food_id: uuid.UUID
    nutrition_id: uuid.UUID
    value: float
    
class FoodNutritionCreate(FoodNutritionBaseModel):
    pass