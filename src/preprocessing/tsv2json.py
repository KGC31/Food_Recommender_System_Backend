import csv
import json
import sys
import pandas as pd
from config import DATASET_FOLDER_PATH, DATASET_LIST

SELECTED_FIELDS = [
    "id",
    "name",
    "alternate_names",
    "description",
    "serving",
    "nutrition_100g",
    "ingredients",
]

def parse_if_json(content):
    if isinstance(content, str) and content.strip().startswith(("{", "[")):
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass
    return content

def tsv_to_json(dataset_folder, filename):
    tsv_file_path = f"{dataset_folder}{filename}"
    json_file_path = f"{dataset_folder}{filename}.json"

    data = []
    with open(tsv_file_path, 'r', encoding='utf-8') as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        for row in reader:
            data.append(row)
            
    df = pd.DataFrame(data)
    df = df[SELECTED_FIELDS]
    
    for column in SELECTED_FIELDS:
        if column in df.columns:
            df[column] = df[column].apply(parse_if_json)
    
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(
            df.to_dict(orient="records"),
            json_file,
            ensure_ascii=False,
            indent=4
        )
        
def main(args):
    if len(args) == 0:
        print("No arguments provided.")
        return
    
    # Processing for datset folder and name
    dataset = args[0]
    if dataset not in DATASET_LIST:
        print(f"Dataset '{dataset}' is not in the allowed dataset list.")
        return
    
    dataset_folder = DATASET_FOLDER_PATH + "/" + dataset + "/"
    
    filename = args[1]
    if not filename.endswith(".tsv"):
        print("Provided file is not a TSV file.")
        return
    
    tsv_to_json(dataset_folder, filename)
        
if __name__ == "__main__":
    main(sys.argv[1:]) 