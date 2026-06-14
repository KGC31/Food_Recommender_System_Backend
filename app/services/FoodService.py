import logging

# Repositories
from app.repositories.FoodRepository import FoodRepository
from app.repositories.NutritionRepository import NutritionRepository
from app.repositories.FoodNutritionRepository import FoodNutritionRepository

# Models
from app.models.FoodModel import FoodCreate
from app.models.NutritionModel import NutritionCreate
from app.models.FoodNutritionModel import FoodNutritionCreate

# Schemas
from app.db.postgres.schema import FoodMetaData

# Utilities
from app.utils.enums import StatusCodeEnum
from app.utils.helpers import extract_nutrients
from app.utils.enums import MealFactorEnum

class FoodService:
    def __init__(self, db):
        self._session = db
        self.food_repository = FoodRepository(db)
        self.nutrition_repository = NutritionRepository(db)
        self.food_nutrition_repository = FoodNutritionRepository(db)
        
    def create_food(self, data: FoodCreate) -> StatusCodeEnum:
        try:
            with self._session.begin():
                # Get category id for food insertion
                category_id = self.food_repository.get_or_create_category(
                    category_name_vi=data.food_metadata.category_name_vi,
                    category_name_en=data.food_metadata.category_name_en
                ).id
                
                # Create and insert food metadata
                food_metadata = FoodMetaData(
                    name_vi=data.food_metadata.name_vi,
                    name_en=data.food_metadata.name_en,
                    kcal_per_100g=data.food_metadata.kcal_per_100g,
                    kj_per_100g=data.food_metadata.kj_per_100g,
                    source=data.food_metadata.source,
                    source_url=data.food_metadata.source_url,
                    category_id=category_id
                )
                
                food = self.food_repository.create(
                    data = food_metadata
                )

                # Extract nutritrients for nutrient name and nutrient class
                nutrients = extract_nutrients(data)

                for name, nutrition_class, value in nutrients:
                    nutrition_meta = self.nutrition_repository.get_or_create(
                        data=NutritionCreate(
                            nutrition=name,
                            nutrition_class=nutrition_class
                        )
                    )

                    self.food_nutrition_repository.create(
                        data = FoodNutritionCreate(
                            food_id=food.id,
                            nutrition_id=nutrition_meta.id,
                            value=value
                        )
                    )
                    
            return StatusCodeEnum.SUCCESS
        
        except Exception as e:
            print(f"Error creating food: {e}")
            return StatusCodeEnum.INTERNAL_SERVER_ERROR

    def get_foods_by_kcal_range(self, meal_target: float, portion_factor: float) -> list[FoodMetaData]:
        try:
            # Get food list query from repository
            min_kcal = (meal_target * MealFactorEnum.MEAL_LOWER_FACTOR.value) / portion_factor,
            max_kcal = (meal_target * MealFactorEnum.MEAL_UPPER_FACTOR.value) / portion_factor
            
            result = self.food_repository.get_foods_by_kcal_range(min_kcal, max_kcal)
            return result
        except Exception as e:
            logging.error(f"Internal Server Errer: {e}")
            raise e