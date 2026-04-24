from app.models.FoodModel import FoodBaseModel

# ============================
# Helper function to extract nutrients from FoodBaseModel and return a list of tuples containing nutrient name, class, and value.
# paramIn:
#   food_data: FoodBaseModel - The food data containing various nutrition information.
# paramOut:
#   list[tuple[str, str, float]] - A list of tuples containing nutrient name, class, and value.
# ============================
def extract_nutrients(food_data: FoodBaseModel) -> list[tuple[str, str, float]]:
    nutrients = []

    nutrition_groups = [
        food_data.macros_nutrition_info,
        food_data.sugars_nutrition_info,
        food_data.minerals_nutrition_info,
        food_data.vitamins_nutrition_info,
        food_data.carotenoids_nutrition_info,
        food_data.purines_nutrition_info,
        food_data.isoflavones_nutrition_info,
        food_data.lipid_nutrition_info,
        food_data.amino_acids_nutrition_info,
    ]

    for group in nutrition_groups:
        data = group.model_dump()
        nutrition_class = group.get_nutrition_class()

        for key, value in data.items():
            if value is None:
                continue
            nutrients.append((key, nutrition_class, value))

    return nutrients


def food_nutrient_to_obj(food_nutrients: list[dict]) -> dict:
    from collections import defaultdict
    structured = defaultdict(dict)

    for n in food_nutrients:
        nutrition_class = n["nutrition_class"]
        nutrition = n["nutrition"]
        value = n["value"]

        structured[nutrition_class][nutrition] = value

    return structured