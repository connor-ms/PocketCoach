import csv
import os
import dotenv
import sqlalchemy
import supabase

"""
NOTE:
First, usda_branded_500k.csv.zip needs to be unzipped and renamed to usda_branded_500k.csv.
GitHub has a limit of 100MB per file, so the file had to be compressed to be uploaded.
"""


def try_convert(value):
    if value == "":
        return None
    
    try:
        int_value = int(value)
        return int_value
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def import_file_to_db(connection, file_path: str, table: str, batch_size: int):
    to_insert = []

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)

            for line_number, row in enumerate(csvreader, start=2):
                try:
                    converted_row = { key: try_convert(value) for key, value in row.items() }
                    to_insert.append(converted_row)

                    if len(to_insert) >= batch_size:
                        try:
                            connection.table(table).insert(to_insert).execute()
                            print(f"Inserted {len(to_insert)} rows.")
                            to_insert.clear()
                        except Exception as e:
                            print(f"Error inserting data: {e}")

                except Exception as e:
                    print(f"Error on line {line_number}")
                    print(f"Error details: {e}")

    except FileNotFoundError:
        print(f"File {file_path} not found.")

    except Exception as e:
        print(f"An error occurred: {e}")


def apply_schema(schema_path: str):
    db_url = os.environ.get("POSTGRES_URI")
    engine = sqlalchemy.create_engine(db_url)

    with open(schema_path, 'r') as file:
        schema_sql = file.read()

    with engine.connect() as connection:
        with connection.begin() as transaction:
            try:
                connection.execute(sqlalchemy.text(schema_sql))
                print("Schema applied successfully.")
            except Exception as e:
                print("Error applying schema:", e)
                transaction.rollback()


if __name__ == "__main__":
    dotenv.load_dotenv()

    apply_schema("schema.sql")

    BATCH_SIZE = 7000

    url: str = os.environ.get("DB_URL")
    key: str = os.environ.get("DB_KEY")
    connection = supabase.create_client(url, key)

    import_file_to_db(connection, "data/menustat.csv", "menustat", BATCH_SIZE)
    import_file_to_db(connection, "data/usda_branded_500k.csv", "usda_branded", BATCH_SIZE)
    import_file_to_db(connection, "data/usda_non_branded.csv", "usda_non_branded", BATCH_SIZE)