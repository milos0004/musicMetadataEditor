import sqlite3

# Path to the MediaMonkey 5 SQLite database
DB_PATH = r"E:\Mediamonkey 5\Portable\MM5.DB"

def inspect_table_schema(db_path, table_name):
    """Prints the schema of the specified table to help identify available columns."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to get the table schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        print(f"Schema for table '{table_name}':")
        for column in columns:
            print(column)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def main():
    # Inspect the 'Songs' and 'Artists' tables to check their column names
    inspect_table_schema(DB_PATH, "Songs")
    inspect_table_schema(DB_PATH, "Artists")

if __name__ == "__main__":
    main()
