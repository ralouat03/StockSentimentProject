import sqlite3
import os

def create_database_from_schema(schema_file, db_file):
    """
    Creates an SQLite database from a given schema file.

    Args:
        schema_file (str): The path to the schema.sql file.
        db_file (str): The name of the database file to create.
    """
    try:
        with sqlite3.connect(db_file) as conn:
            with open(schema_file, 'r') as f:
                conn.executescript(f.read())
            print(f"Database file '{db_file}' created successfully from schema file '{schema_file}'.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except FileNotFoundError:
        print(f"Error: Schema file '{schema_file}' not found.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(script_dir, 'schema.sql')
    db_file = os.path.join(os.path.dirname(script_dir), 'data', 'sentiment.db')

    create_database_from_schema(schema_file, db_file)
