import psycopg2
import json
import os

# Database connection parameters
DB_CONFIG = {
    'dbname': 'aa',
    'user': 'and',
    'password': '1234',
    'host': 'localhost',
    'port': '5433'
}

OUTPUT_DIR = './dumps/'

def fetch_recipes():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = "SELECT * FROM recipies;"
        cursor.execute(query)

        colnames = [desc[0] for desc in cursor.description]

        rows = cursor.fetchall()

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        for row in rows:
            recipe_dict = dict(zip(colnames, row))

            file_name = f"{recipe_dict['id']}.json"
            file_path = os.path.join(OUTPUT_DIR, file_name)

            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(recipe_dict, json_file, ensure_ascii=False, indent=4)

        print(f"Dumped {len(rows)} recipes to {OUTPUT_DIR}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    fetch_recipes()
