import ollama
import json
import logging
from pydantic import BaseModel

from app.db.neo4j.connection import neo4j_conn

# Definition for food tags retrival result
class FoodTags(BaseModel):
    food_groups: list[str] = []
    macro_profile: list[str] = []
    medical_tags: list[str] = []
    dietary_restrictions: list[str] = []
    cuisine_tags: list[str] = []

# Generate tags for food
def extract_key_nutrition(nutrition):
    keys = [
        "calories",
        "protein",
        "carbohydrates",
        "total_fat",
        "saturated_fats",
        "dietary_fiber",
        "total_sugars",
        "sodium",
        "cholesterol"
    ]

    return {k: nutrition.get(k) for k in keys if k in nutrition}

def generate_tags(food):
    prompt = f"""
    You are a strict classifier.

    You MUST only output tags from the allowed lists.
    If a tag is not in the allowed list, DO NOT generate it.

    Do not invent tags.

    Return JSON only.

    Allowed values:

    food_groups:
    fruits, vegetables, grains, whole_grains, refined_grains,
    legumes, nuts_seeds, meat, poultry, fish_seafood,
    eggs, dairy, plant_based_protein, mixed_dish

    macro_profile:
    high_protein, high_fiber, high_fat, high_carb, low_carb, low_fat, balanced_macros

    macro rules:
    high_protein → protein ≥ 15g
    high_fiber → fiber ≥ 5g
    high_carb → carbs ≥ 50g
    low_carb → carbs ≤ 10g
    low_fat → fat ≤ 3g
    high_fat → fat ≥ 20g

    medical_tags:
    diabetic_friendly, heart_healthy, low_sodium, low_cholesterol,
    renal_friendly, gut_friendly, anti_inflammatory,
    weight_loss, weight_gain, high_calorie, low_calorie

    dietary_restrictions:
    vegetarian, vegan, pescatarian, gluten_free, dairy_free,
    nut_free, soy_free, egg_free, halal, kosher
    
    Cuisine tags must be ONLY country or continent names.
    Allowed examples:
    italy, vietnam, china, japan, korea, india,
    mexico, france, spain, thailand, usa,
    europe, asia, africa, south_america, north_america

    Rules:
    - only allowed tags
    - no extra tags
    - omit uncertain tags
    - cuisine_tags only if the food is strongly associated with a cuisine
    - most foods have no cuisine tag
    - output JSON only

    {{
        "food_groups": [],
        "macro_profile": [],
        "medical_tags": [],
        "dietary_restrictions": [],
        "cuisine_tags": []
    }}

    Food Information:
    Name: {food["name"]}
    Description: {food["description"]}
    Ingredients: {food["ingredients"]}
    Nutrition per 100g: {extract_key_nutrition(food["nutrition_100g"])}
    """

    logging.info(f"Generating tags for: {food['name']}")
    messages = [
        {"role": "user", "content": prompt}
    ]
    messages = messages[-3:]

    response = ollama.chat(
        model="gpt-oss:20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        },
        format=FoodTags.model_json_schema()
    )
    
    content = response["message"]["content"]
    print(f"Raw response content: {content}")  # Debugging line to check the raw response

    # remove markdown code fences if present
    content = content.replace("```json", "").replace("```", "").strip()

    return json.loads(content)

# Insert food and tags into Neo4j
def insert_food_with_tags(food, tags):
    logging.info(f"Inserting food into Neo4j: {food['name']}")

    query = """
    MERGE (f:Food {name: $name})
    SET f.description = $description,
        f.ingredients = $ingredients

    WITH f

    UNWIND keys($nutrition) AS nutrient_name
    MERGE (n:Nutrient {name: nutrient_name})
    MERGE (f)-[:HAS_NUTRIENT {amount: $nutrition[nutrient_name]}]->(n)

    WITH f

    UNWIND $food_groups AS fg_name
    MERGE (fg:FoodGroup {name: fg_name})
    MERGE (f)-[:BELONGS_TO]->(fg)

    WITH f

    UNWIND $macro_profile AS macro_name
    MERGE (m:MacroProfile {name: macro_name})
    MERGE (f)-[:HAS_MACRO]->(m)

    WITH f

    UNWIND $medical_tags AS mt_name
    MERGE (mt:MedicalTag {name: mt_name})
    MERGE (f)-[:HAS_MEDICAL_TAG]->(mt)

    WITH f

    UNWIND $dietary_restrictions AS dr_name
    MERGE (dr:DietaryRestriction {name: dr_name})
    MERGE (f)-[:HAS_DIETARY_RESTRICTION]->(dr)

    WITH f

    UNWIND $cuisine_tags AS ct_name
    MERGE (ct:CuisineTag {name: ct_name})
    MERGE (f)-[:HAS_CUISINE_TAG]->(ct)
    """

    with neo4j_conn.driver.session() as session:
        session.run(
            query,
            name=food["name"],
            description=food["description"],
            ingredients=food["ingredients"],
            nutrition=food["nutrition_100g"],
            food_groups=tags.get("food_groups", []),
            macro_profile=tags.get("macro_profile", []),
            medical_tags=tags.get("medical_tags", []),
            dietary_restrictions=tags.get("dietary_restrictions", []),
            cuisine_tags=tags.get("cuisine_tags", []),
        )
        
# Load food data from JSON file
def load_foods_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def food_exists(tx, name):
    query = """
    MATCH (f:Food {name: $name})
    RETURN f LIMIT 1
    """
    result = tx.run(query, name=name)
    return result.single() is not None

def food_exists_in_db(driver, name):
    with driver.session() as session:
        return session.execute_read(food_exists, name)
    
if __name__ == "__main__":
    # load food data from JSON file
    json_path = r"G:\Code\Food_Recommender_System\data\opennutrition\opennutrition_foods.tsv.json"

    food_data = load_foods_from_json(json_path)

    for food_json in food_data:
        try:
            if food_exists_in_db(neo4j_conn.driver, food_json["name"]):
                logging.info(f"Skipping existing food: {food_json['name']}")
                continue

            tags = generate_tags(food_json)
            logging.info(f"Generated tags for {food_json['name']}: {tags}")

            insert_food_with_tags(food_json, tags)

        except Exception as e:
            logging.error(f"Failed to process {food_json['name']}: {e}")