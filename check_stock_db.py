import sqlite3
import os

# --- Configuration ---
DB_FILENAME = "stock_data.db"       # SQLite database file name to connect to
TABLE_NAME = "stock_prices"         # Name of the table to query
LIMIT = 5                           # Number of rows to fetch and display
# --- ---

def check_database(db_path, table_name, limit):
    """
    Connects to the SQLite database and prints the first 'limit' rows from the specified table.
    """
    if not os.path.exists(db_path):
        print(f"Error: Database file not found: {db_path}")
        print("Please run the create_stock_db.py script first to create the database.")
        return

    print(f"Connecting to SQLite database: {db_path}...")
    try:
        # Use 'with' for automatic connection closing
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            print(f"Executing query: SELECT * FROM {table_name} LIMIT {limit}")

            # Execute the query
            query = f"SELECT * FROM {table_name} LIMIT ?"
            cursor.execute(query, (limit,)) # Use parameterized query for safety

            # Fetch column names
            col_names = [description[0] for description in cursor.description]
            print("\nColumn names:", col_names)

            # Fetch the results
            rows = cursor.fetchall()

            if not rows:
                print(f"\nTable '{table_name}' is empty or does not exist.")
            else:
                print(f"\nFirst {len(rows)} rows from table '{table_name}':")
                # Print each row
                for i, row in enumerate(rows):
                    print(f"Row {i+1}: {row}")

    except sqlite3.Error as e:
        # Catch specific SQLite errors (like 'no such table')
        print(f"Error working with SQLite: {e}")
        if "no such table" in str(e).lower():
             print(f"Make sure a table named '{table_name}' exists in the database.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    check_database(DB_FILENAME, TABLE_NAME, LIMIT)
    print("\nScript finished.")