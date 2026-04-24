from pydantic import BaseModel

from app.utils.enums import FoodAllergyTypeEnum, DietaryPreferenceEnum

class PatientHealthMetrics(BaseModel):
    age: int
    gender: str
    weight_kg: float
    height_cm: float
    activity_factor: float = 1.2
    portion_size_g: float = 1.0
    allergies: list[FoodAllergyTypeEnum]
    dietary_preferences: list[DietaryPreferenceEnum]
    
