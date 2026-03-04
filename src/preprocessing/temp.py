import json

unique_nutrients = set()

with open(r"C:\Users\kimcu\Documents\Codes\Project\Food_Recommender_System\Dataset\opennutrition\opennutrition_foods.tsv.json", 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    
for item in data:
    for key, value in item["nutrition_100g"].items():
        unique_nutrients.add(key)
        
print(unique_nutrients)