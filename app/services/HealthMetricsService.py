from app.core.fuzzy.membership import trapezoid, triangle
from app.utils.enums import TargetWeightCalorieAdjustmentEnum, WeightThreshold

class HealthMetricsService:
    def __init__(self):
        pass
    
    def bmi_memberships(self, bmi: float) -> dict:
        return {
            "underweight": trapezoid(bmi, 0, 0, 16, 18.5),
            "normal_weight": triangle(bmi, 18.0, 22.0, 25.0),
            "overweight": triangle(bmi, 23.0, 25.0, 30.0),
            "obesity_class_I": triangle(bmi, 28.0, 32.5, 35.0),
            "obesity_class_II": triangle(bmi, 33.0, 37.5, 40.0),
            "obesity_class_III": trapezoid(bmi, 38.0, 42.0, 60.0, 60.0),
        }

    def calculate_bmi(self, weight_kg: float, height_cm: float) -> float:
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 2)

    # Mifflin-St Jeor Equation
    def calculate_bmr(self, weight_kg: float, height_cm: float, age: int, gender: str) -> float:
        if gender.lower() == "male":
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        elif gender.lower() == "female":
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
        else:
            raise ValueError("Gender must be 'male' or 'female'")
        return round(bmr, 2)
    
    def weight_health_condition_diagnosis(self, bmi: float) -> str: 
        memberships = self.bmi_memberships(bmi) 
        return max(memberships, key=memberships.get)
    
    def calculate_calorie_target(self, bmi: float, bmr: float, activity_factor: float) -> int:
        tdee = bmr * activity_factor
        memberships = self.bmi_memberships(bmi)

        adjustment = (
            memberships["underweight"] * TargetWeightCalorieAdjustmentEnum.STANDARD_GAIN_WEIGHT.value +
            memberships["normal_weight"] * TargetWeightCalorieAdjustmentEnum.MAINTAIN_WEIGHT.value +
            memberships["overweight"] * TargetWeightCalorieAdjustmentEnum.STANDARD_LOSE_WEIGHT.value +
            memberships["obesity_class_I"] * TargetWeightCalorieAdjustmentEnum.STANDARD_LOSE_WEIGHT.value * 1.5 +
            memberships["obesity_class_II"] * TargetWeightCalorieAdjustmentEnum.STANDARD_LOSE_WEIGHT.value * 2 +
            memberships["obesity_class_III"] * TargetWeightCalorieAdjustmentEnum.STANDARD_LOSE_WEIGHT.value * 2.5
        )

        return int(tdee + adjustment)
