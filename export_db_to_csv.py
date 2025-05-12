# --- START OF FILE export_db_to_csv.py ---

import pandas as pd
import sqlite3
import os

# --- Configuration ---
DB_FILENAME = "stock_data.db"          # SQLite database file to read from
TABLE_NAME = "stock_prices"            # Name of the table to read
CSV_EXPORT_FILENAME = "stock_data_export.csv" # Output CSV file name
# --- ---

def export_table_to_csv(db_path, table_name, csv_path):
    """
    Reads data from an SQLite table and exports it to a CSV file.
    """
    if not os.path.exists(db_path):
        print(f"Error: Database file not found: {db_path}")
        print("Please run the 'fetch_and_store_prices.py' script first.")
        return

    print(f"Connecting to database: {db_path}")
    try:
        with sqlite3.connect(db_path) as conn:
            print(f"Reading data from table: '{table_name}'...")
            # Use pandas read_sql_query for convenience
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, conn)

            if df.empty:
                print(f"Table '{table_name}' is empty. No data to export.")
                return

            print(f"Read {len(df)} rows from the database.")
            print(f"Exporting data to CSV file: {csv_path}...")

            # Export to CSV
            # index=False: Don't write the DataFrame index
            # encoding='utf-8-sig': Good for compatibility, especially with Excel (handles BOM)
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')

            print(f"Data successfully exported to {csv_path}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        if "no such table" in str(e).lower():
             print(f"Ensure the table '{table_name}' exists in the database.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    export_table_to_csv(DB_FILENAME, TABLE_NAME, CSV_EXPORT_FILENAME)
    print("\nExport script finished.")

# --- END OF FILE export_db_to_csv.py ---