from enum import Enum

class ActivityLevel(Enum):
    SEDENTARY = 1.2
    LIGHTLY_ACTIVE = 1.375
    MODERATELY_ACTIVE = 1.55
    VERY_ACTIVE = 1.725
    EXTRA_ACTIVE = 1.9
    
class WeightThreshold(Enum):
    UNDERWEIGHT = 18.5
    NORMAL_WEIGHT = 24.9
    OVERWEIGHT = 29.9
    OBESITY_I = 30.0
    OBESITY_II = 35.0
    OBESITY_III = 40.0
    
# Calorie adjustments for different weight goals (gain/lose weight) based on general guidelines
class TargetWeightCalorieAdjustmentEnum(Enum):
    LITTLE_GAIN_WEIGHT = 300
    STANDARD_GAIN_WEIGHT = 500
    LITTLE_LOSE_WEIGHT = -300
    STANDARD_LOSE_WEIGHT = -500
    MAINTAIN_WEIGHT = 0
    
# Meal factors to adjust daily calorie needs based on meal size and frequency
class MealFactorEnum(Enum):
    MEAL_LOWER_FACTOR = 0.6
    MEAL_UPPER_FACTOR = 1.4
    
# Permitted Nutrition Claims based on EU regulations (Regulation (EC) No 1924/2006)
# https://food.ec.europa.eu/food-safety/labelling-and-nutrition/nutrition-and-health-claims/nutrition-claims_en
class PermittedNutritionClaimsEnum(Enum):
    # ENERGY
    LOW_ENERGY = "LOW ENERGY"
    ENERGY_FREE = "ENERGY FREE"

    # FAT
    LOW_FAT = "LOW FAT"
    FAT_FREE = "FAT FREE"

    # SAT FAT
    LOW_SATURATED_FAT = "LOW SATURATED FAT"
    SATURATED_FAT_FREE = "SATURATED FAT FREE"

    # SUGAR
    LOW_SUGARS = "LOW SUGARS"
    SUGARS_FREE = "SUGARS FREE"

    # SODIUM
    LOW_SODIUM = "LOW SODIUM"
    VERY_LOW_SODIUM = "VERY LOW SODIUM"
    SODIUM_FREE = "SODIUM FREE"

    # FIBRE
    SOURCE_OF_FIBRE = "SOURCE OF FIBRE"
    HIGH_FIBRE = "HIGH FIBRE"

    # PROTEIN
    SOURCE_OF_PROTEIN = "SOURCE OF PROTEIN"
    HIGH_PROTEIN = "HIGH PROTEIN"

    # OMEGA 3
    SOURCE_OF_OMEGA_3_FATTY_ACIDS = "SOURCE OF OMEGA-3 FATTY ACIDS"

    # FAT QUALITY
    HIGH_MONOUNSATURATED_FAT = "HIGH MONOUNSATURATED FAT"
    HIGH_POLYUNSATURATED_FAT = "HIGH POLYUNSATURATED FAT"
    HIGH_UNSATURATED_FAT = "HIGH UNSATURATED FAT"
    
class FoodAllergyTypeEnum(Enum):
    GLUTEN = "GLUTEN"
    PEANUTS = "PEANUTS"
    TREE_NUTS = "TREE NUTS"
    DAIRY = "DAIRY"
    EGGS = "EGGS"
    FISH = "FISH"
    SHELLFISH = "SHELLFISH"
    SOY = "SOY"
    SESAME = "SESAME"
    
class DietaryPreferenceEnum(Enum):
    VEGETARIAN = "VEGETARIAN"
    VEGAN = "VEGAN"
    PESCATARIAN = "PESCATARIAN"
    HALAL = "HALAL"
    KOSHER = "KOSHER"
    
class FiveFoodGroupsEnum(Enum):
    FRUITS = "FRUITS"
    VEGETABLES = "VEGETABLES"
    GRAINS = "GRAINS"
    PROTEINS = "PROTEINS"
    DAIRY = "DAIRY"
    
class NutritionClassEnum(Enum):
    MACROS = "MACROS"
    SUGARS = "SUGARS"
    MINERALS = "MINERALS"
    VITAMINS = "VITAMINS"
    CAROTENOIDS = "CAROTENOIDS"
    PURINES = "PURINES"
    ISOFLAVONES = "ISOFLAVONES"
    LIPIDS = "LIPIDS"
    AMINO_ACIDS = "AMINO ACIDS"
    
class MacrosEnum(Enum):
    WATER = "WATER"
    PROTEIN = "PROTEIN"
    FATS = "FATS"
    CARBOHYDRATES = "CARBOHYDRATES"
    FIBRE = "FIBRE"
    ASH = "ASH"
    
class SugarsEnum(Enum):
    TOTAL_SUGARS = "TOTAL SUGARS"
    GALACTOSE = "GALACTOSE"
    MALTOSE = "MALTOSE"
    LACTOSE = "LACTOSE"
    FRUCTOSE = "FRUCTOSE"
    GLUCTOSE = "GLUCTOSE"
    SUCROSE = "SUCROSE"
    
class MineralsEnum(Enum):
    CALCIUM = "CALCIUM"
    IRON = "IRON"
    MAGNESIUM = "MAGNESIUM"
    PHOSPHORUS = "PHOSPHORUS"
    POTASSIUM = "POTASSIUM"
    SODIUM = "SODIUM"
    ZINC = "ZINC"
    COPPER = "COPPER"
    SELENIUM = "SELENIUM"
    
class VitaminsEnum(Enum):
    VITAMIN_A = "VITAMIN A"
    VITAMIN_B1 = "VITAMIN B1"
    VITAMIN_B2 = "VITAMIN B2"
    VITAMIN_B5 = "VITAMIN B5"
    VITAMIN_B6 = "VITAMIN B6"
    VITAMIN_B9 = "VITAMIN B9"
    VITAMIN_B12 = "VITAMIN B12"
    VITAMIN_C = "VITAMIN C"
    VITAMIN_D = "VITAMIN D"
    VITAMIN_E = "VITAMIN E"
    VITAMIN_K = "VITAMIN K"
    FOLATE = "FOLATE"
    BIOTIN = "BIOTIN"
    
class CarotenoidsEnum(Enum):
    BETA_CAROTENE = "BETA-CAROTENE"
    ALPHA_CAROTENE = "ALPHA-CAROTENE"
    LYCOPENE = "LYCOPENE"
    LUTEIN_AND_ZEAXANTHIN = "LUTEIN AND ZEAXANTHIN"
    
class PurinesEnum(Enum):
    PURINES = "PURINES"
    
class IsoflavonesEnum(Enum):
    TOTAL_ISOFLAVONES = "TOTAL ISOFLAVONES" 
    
class StatusCodeEnum(Enum):
    SUCCESS = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500