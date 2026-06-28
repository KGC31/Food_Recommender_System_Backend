import logging
from app.models.FoodModel import *
from app.models.NutritionModel import *

# Services
from app.services.HealthMetricsService import HealthMetricsService
from app.services.NutritionService import NutritionService
from app.services.FoodService import FoodService

# Utilities
from app.utils.types import PatientHealthMetrics
from app.utils.helpers import food_nutrient_to_obj

class RecommenderService:
    def __init__(self, db):
        self._session = db
        self.nutrition_service = NutritionService(db)
        self.health_metrics_service = HealthMetricsService()
        self.food_service = FoodService(db)
        
    def extract_tags(self, patient_profile: PatientHealthMetrics):
        medical_tags = []
        dietary_tags = []

        if patient_profile.has_diabetes:
            medical_tags.append("diabetes")

        if patient_profile.goal == "weight_loss":
            dietary_tags.append("low_calorie")

        if patient_profile.goal == "muscle_gain":
            dietary_tags.append("high_protein")

        return medical_tags, dietary_tags
    
    def get_recommended_foods(self, user_metrics: FoodRecommendationRequest) -> list[FoodBaseModel]:
        try:
            result = []
            bmi = self.health_metrics_service.calculate_bmi(user_metrics.weight_kg, user_metrics.height_cm)
            bmr = self.health_metrics_service.calculate_bmr(user_metrics.weight_kg, user_metrics.height_cm, user_metrics.age, user_metrics.gender)
            
            # Target calorie (kcal/day)
            calorie_target = self.health_metrics_service.calculate_calorie_target(bmi, bmr, user_metrics.activity_factor)
            meal_target = calorie_target / 3
            portion_factor = user_metrics.portion_size_g / 100

            foods = self.food_service.get_foods_by_kcal_range(meal_target, portion_factor)
            nutrients = self.nutrition_service.get_nutrients_by_food_ids([food.id for food in foods])
            
            for food in foods:
                food_nutrients = [nutrient for nutrient in nutrients if nutrient["food_id"] == food.id]
                food_nutrients_obj = food_nutrient_to_obj(food_nutrients)
                
                object = FoodBaseModel(
                    food_metadata=FoodMetaData(
                        name_vi=food["name_vi"],
                        name_en=food["name_en"],
                        kcal_per_100g=food["kcal_per_100g"],
                        kj_per_100g=food["kj_per_100g"],
                        source=food["source"],
                        source_url=food["source_url"],
                    ),

                    macros_nutrition_info=MacrosNutritionInfo(**food_nutrients_obj.get("macros_nutrition_info", {})),
                    sugars_nutrition_info=SugarsNutritionInfo(**food_nutrients_obj.get("sugars_nutrition_info", {})),
                    minerals_nutrition_info=MineralsNutritionInfo(**food_nutrients_obj.get("minerals_nutrition_info", {})),
                    vitamins_nutrition_info=VitaminsNutritionInfo(**food_nutrients_obj.get("vitamins_nutrition_info", {})),
                    carotenoids_nutrition_info=CarotenoidsNutritionInfo(**food_nutrients_obj.get("carotenoids_nutrition_info", {})),
                    purines_nutrition_info=PurinesNutritionInfo(**food_nutrients_obj.get("purines_nutrition_info", {})),
                    isoflavones_nutrition_info=IsoflavonesNutritionInfo(**food_nutrients_obj.get("isoflavones_nutrition_info", {})),
                    lipid_nutrition_info=LipidNutritionInfo(**food_nutrients_obj.get("lipid_nutrition_info", {})),
                    amino_acids_nutrition_info=AminoAcidsNutritionInfo(**food_nutrients_obj.get("amino_acids_nutrition_info", {})),
                )
                
                result.append(object)
                
            return result
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            raise e