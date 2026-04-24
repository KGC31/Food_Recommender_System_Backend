from pydantic import BaseModel

from app.utils.types import *
from app.models.NutritionModel import *

class FoodMetaData(BaseModel):
    name_vi: str
    name_en: str
    kcal_per_100g: float
    kj_per_100g: float
    
class FoodBaseModel(BaseModel):
    food_metadata:              FoodMetaData
    macros_nutrition_info:      MacrosNutritionInfo
    sugars_nutrition_info:      SugarsNutritionInfo
    minerals_nutrition_info:    MineralsNutritionInfo
    vitamins_nutrition_info:    VitaminsNutritionInfo
    carotenoids_nutrition_info: CarotenoidsNutritionInfo
    purines_nutrition_info:     PurinesNutritionInfo
    isoflavones_nutrition_info: IsoflavonesNutritionInfo
    lipid_nutrition_info:       LipidNutritionInfo
    amino_acids_nutrition_info: AminoAcidsNutritionInfo
    
class FoodCreate(FoodBaseModel):
    pass

class FoodRecommendationRequest(BaseModel):
    age: int
    gender: str
    weight_kg: float
    height_cm: float
    activity_factor: float = 1.2
    portion_size_g: float = 1.0
    allergies: list[FoodAllergyTypeEnum]
    dietary_preferences: list[DietaryPreferenceEnum]
    
class FoodRecommendationResponse(BaseModel):
    recommended_foods: list[FoodBaseModel]