import pandas as pd
import sqlite3
import os

# --- Configuration ---
CSV_FILENAME = "stock_data_3years_yfinance_with_names.csv" # Input CSV file name
DB_FILENAME = "stock_data.db"                            # Output SQLite database file name
TABLE_NAME = "stock_prices"                              # Name of the table within the database
# --- ---

def create_database_from_csv(csv_path, db_path, table_name):
    """
    Reads data from a CSV file and saves it into an SQLite table.
    If the table already exists, it will be replaced (dropped and recreated).
    """
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at path: {csv_path}")
        return

    print(f"Reading data from CSV file: {csv_path}...")
    try:
        # Read the CSV into a pandas DataFrame
        df = pd.read_csv(csv_path)
        print(f"Read {len(df)} rows.")

        # Check for essential columns (add more checks if needed)
        required_columns = ['ticker', 'company_name', 'date', 'o', 'h', 'l', 'c']
        if not all(col in df.columns for col in required_columns):
            print(f"Error: CSV file is missing some required columns: {required_columns}")
            missing = [col for col in required_columns if col not in df.columns]
            print(f"Missing columns: {missing}")
            return

        print(f"Connecting to SQLite database: {db_path}...")
        # Create a connection to the DB (the file will be created if it doesn't exist)
        # Use 'with' to ensure the connection is closed automatically
        with sqlite3.connect(db_path) as conn:
            print(f"Writing data to table '{table_name}'...")
            # Use the pandas to_sql method for easily writing the DataFrame to the DB
            # if_exists='replace': drop the table if it exists, then create a new one
            # index=False: do not write the DataFrame index as a column in the DB
            df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)

            # Optional: Create an index to speed up queries on ticker and date
            print(f"Creating index for table '{table_name}' on (ticker, date)...")
            cursor = conn.cursor()
            cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_ticker_date ON {table_name} (ticker, date);")
            conn.commit() # Save index changes

            print("Data successfully loaded into the database.")
            print(f"Table '{table_name}' created/replaced.")

    except pd.errors.EmptyDataError:
        print(f"Error: CSV file '{csv_path}' is empty.")
    except sqlite3.Error as e:
        print(f"Error working with SQLite: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    create_database_from_csv(CSV_FILENAME, DB_FILENAME, TABLE_NAME)
    print(f"\nScript finished. Database '{DB_FILENAME}' should be created/updated.")