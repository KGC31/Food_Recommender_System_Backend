import psycopg2
import json
import sys
from config import DATASET_FOLDER_PATH, DATASET_LIST

def get_unique_nutrients(json_file_path):
    unique_nutrients = set()
    
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        
    for item in data:
        for key, value in item["nutrition_100g"].items():
            unique_nutrients.add(key)
            
    return unique_nutrients

def create_table_if_not_exists(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS food_metadata (
            id TEXT PRIMARY KEY,
            name TEXT,
            alternate_names JSONB,
            description TEXT,
            ingredients JSONB
        )
        """
    )
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS nutrition_metadata (
            id TEXT PRIMARY KEY,
            nutrition TEXT,
        )
        """
    )
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS food_nutrients (
            id TEXT PRIMARY KEY,
            food_id TEXT,
            nutrition_id TEXT,
            value FLOAT,
            FOREIGN KEY (food_id) REFERENCES food_metadata (id),
            FOREIGN KEY (nutrition_id) REFERENCES nutrition_metadata (id)
        )
        """
    )

def insert_data_to_postgres(dataset_folder, filename):
    json_file_path = f"{dataset_folder}{filename}.json"
    
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    # Database connection parameters
    db_params = {
        "dbname": "opennutrition",
        "user": "postgres",
        "password": "Kimcurry17112003",
        "host": "localhost",
        "port": 5432
    }
    
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        create_table_if_not_exists(cursor)
        
        #  Get unique nutrients and create columns for them
        unique_nutrients = get_unique_nutrients(json_file_path)
        
        for nutrient in unique_nutrients:
            cursor.execute(
                f"""
                INSERT INTO nutrition_metadata (nutrient)
                VALUES (%s)
                """,
                (
                    nutrient
                )
            )
        
        cursor.execute("SELECT id, nutrient FROM nutrition_metadata")
        nutrient_map = {name: nid for nid, name in cursor.fetchall()}

        # Insert data into the database
        for item in data:
            cursor.execute(
                """
                INSERT INTO food_items (name, alternate_names, description, ingredients)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    item.get("name"),
                    json.dumps(item.get("alternate_names")),
                    item.get("description"),
                    json.dumps(item.get("ingredients"))
                )
            )
            
            food_id = cursor.fetchone()[0]
            
            for nutrient, value in item.get("nutrition_100g", {}).items():
                nutrition_id = nutrient_map.get(nutrient)
                if nutrition_id is None:
                    continue

                cursor.execute(
                    """
                    INSERT INTO food_nutrients (food_id, nutrition_id, value)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (food_id, nutrition_id) DO NOTHING
                    """,
                    (food_id, nutrition_id, value)
                )
        
        # Commit the transaction
        conn.commit()
        
    except Exception as e:
        print(f"Error inserting data into database: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

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
    
    insert_data_to_postgres(dataset_folder, filename)
    
        
if __name__ == "__main__":
    main(sys.argv[1:]) 