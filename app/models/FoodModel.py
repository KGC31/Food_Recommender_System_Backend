from pydantic import BaseModel

from app.utils.types import *
from app.models.NutritionModel import *

class FoodMetaData(BaseModel):
    name_vi:                    str = ""
    name_en:                    str = ""
    kcal_per_100g:              float = 0.0
    kj_per_100g:                float = 0.0
    source:                     str = ""
    source_url:                 str = ""
    category_name_vi:           str = ""
    category_name_en:           str = ""


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
    age:                        int = 0
    gender:                     str = "male"
    weight_kg:                  float = 0.0
    height_cm:                  float = 0.0
    activity_factor:            float = 1.2
    portion_size_g:             float = 1.0
    allergies:                  list[FoodAllergyTypeEnum] = []
    dietary_preferences:        list[DietaryPreferenceEnum] = []
    
class FoodRecommendationResponse(BaseModel):
    recommended_foods: list[FoodBaseModel]