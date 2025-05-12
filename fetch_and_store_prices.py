# --- START OF FILE fetch_and_store_prices.py ---

import yfinance as yf
import pandas as pd
import datetime
import time
import sqlite3
import os

# --- Configuration ---
DB_FILENAME = "stock_data.db"       # SQLite database file name
TABLE_NAME = "stock_prices"         # Name of the table within the database
YEARS_OF_DATA = 5                   # Number of years of historical data to fetch
BATCH_SIZE = 10                     # Optional: Process tickers in batches (can adjust)
                                    # Set to 1 to process one by one if preferred
                                    # Set to large number (e.g., 1000) to process all at once at the end
# --- ---

# Company raw data (same as before)
companies_raw_data = """
Ticker,Company
AAPL,Apple Inc
005930.KS,Samsung Electronics
SONY,Sony Group Corporation
DELL,Dell Technologies
HPQ,HP Inc
0992.HK,Lenovo Group
2357.TW,Quanta Computer
2353.TW,Pegatron Corporation
MSFT,Microsoft Corporation
GOOGL,Alphabet Inc Google
INTC,Intel Corporation
AMD,Advanced Micro Devices Inc
NVDA,NVIDIA Corporation
QCOM,Qualcomm Incorporated
AVGO,Broadcom Inc
TXN,Texas Instruments
MU,Micron Technology Inc
000660.KQ,SK hynix
TSM,Taiwan Semiconductor Manufacturing Company TSMC
ASML,ASML Holding
LOGI,Logitech International SA
CRSR,Corsair Gaming Inc
WDC,Western Digital Corporation
STX,Seagate Technology
NTAP,NetApp Inc
ANET,Arista Networks Inc
SMCI,Super Micro Computer Inc
PSTG,Pure Storage Inc
CAN,Canaan Inc
DDD,D Systems Corporation
CAJ,Canon Inc
6752.T,Panasonic Corporation
066570.KQ,LG Electronics
6502.T,Toshiba Corporation
6702.T,Fujitsu Limited
6701.T,NEC Corporation
6501.T,Hitachi Ltd
6503.T,Mitsubishi Electric Corporation
6971.T,Kyocera Corporation
SIE.DE,Siemens AG
ABB,ABB Ltd
SU.PA,Schneider Electric
ETN,Eaton Corporation
ROK,Rockwell Automation Inc
HON,Honeywell International Inc
EMR,Emerson Electric Co
GE,General Electric Company
PHIA.AS,Koninklijke Philips NV
TDY,Teledyne Technologies Incorporated
IBM,International Business Machines Corporation
ARM,Arm Holdings
NXPI,NXP Semiconductors
ADI,Analog Devices Inc
IFX.DE,Infineon Technologies AG
STM,STMicroelectronics
ON,ON Semiconductor Corporation
MRVL,Marvell Technology Inc
MCHP,Microchip Technology Incorporated
SWKS,Skyworks Solutions Inc
ZBRA,Zebra Technologies Corporation
GRMN,Garmin Ltd
GPRO,GoPro Inc
TRMB,Thermo Fisher Scientific
HEXA-B.ST,Hexagon AB
AMBA,Ambarella Inc
MPWR,Monolithic Power Systems Inc
LRCX,Lam Research Corporation
KLAC,KLA Corporation
TER,Teradyne Inc
COHR,Coherent Inc
MTSI,MACOM Technology Solutions Holdings Inc
DIOD,Diodes Incorporated
SYNA,Synaptics Incorporated
NVMI,Nova Measuring Instruments Ltd
UMC,United Microelectronics Corporation
HIMX,Himax Technologies Inc
AEHR,AEHR Test Systems
ACLS,Axcelis Technologies Inc
CAMT,Camtek Ltd
SMTC,Semtech Corporation
FORM,FormFactor Inc
ICHR,Ichor Systems Inc
LSCC,Lattice Semiconductor Corporation
LITE,Lumentum Holdings Inc
IPGP,IPG Photonics Corporation
MKSI,MKS Instruments Inc
VSH,Vishay Intertechnology Inc
VECO,Veeco Instruments Inc
CRUS,Cirrus Logic Inc
POWI,Power Integrations Inc
WOLF,Wolfspeed Inc
QRVO,Qorvo Inc
OLED,Universal Display Corporation
FLEX,Flex Ltd
BHE,Benchmark Electronics Inc
SANM,Sanmina Corporation
FN,Fabrinet
"""

def parse_company_data(raw_data):
    """Parses the raw company string into a map and ordered list."""
    ticker_to_company_map = {}
    ordered_tickers = []
    for line in raw_data.strip().split('\n'):
        if line.startswith("Ticker,Company") or line.startswith("#") or not line.strip():
            continue
        parts = line.split(',', 1) # Split only on the first comma
        if len(parts) == 2:
            ticker = parts[0].strip()
            company_name = parts[1].strip()
            if ticker and ticker not in ticker_to_company_map: # Add if ticker is not already present
                ticker_to_company_map[ticker] = company_name
                ordered_tickers.append(ticker)
    return ticker_to_company_map, ordered_tickers

def fetch_and_prepare_data(symbol, company_name, start_date_str, end_date_str):
    """Fetches data for a single ticker and prepares the DataFrame."""
    print(f"Fetching data for: {symbol} ({company_name})...")
    try:
        ticker_obj = yf.Ticker(symbol)
        hist_data = ticker_obj.history(start=start_date_str,
                                       end=end_date_str,
                                       interval="1d",
                                       auto_adjust=False # Important for getting 'Close'
                                      )

        if hist_data.empty:
            print(f"  No data found for {symbol} ({company_name}) in the specified period.")
            return None

        hist_data.reset_index(inplace=True)
        hist_data['ticker'] = symbol
        hist_data['company_name'] = company_name

        # Rename columns
        hist_data.rename(columns={
            'Date': 'date', 'Open': 'o', 'High': 'h', 'Low': 'l', 'Close': 'c', 'Volume': 'v'
        }, inplace=True)

        # Ensure 'date' is string YYYY-MM-DD
        # Convert to datetime first to handle potential timezone info from yfinance
        hist_data['date'] = pd.to_datetime(hist_data['date']).dt.strftime('%Y-%m-%d')

        # Calculate 'pc' (Previous Close)
        hist_data['pc'] = hist_data['c'].shift(1)

        # Calculate 'd' (Change) and 'dp' (Percent Change)
        # Initialize with NaN or None is better than 0 for clarity
        hist_data['d'] = pd.NA
        hist_data['dp'] = pd.NA

        # Calculate only where previous close is valid and non-zero
        valid_pc_indices = hist_data['pc'].notna() & (hist_data['pc'] != 0)
        hist_data.loc[valid_pc_indices, 'd'] = hist_data.loc[valid_pc_indices, 'c'] - hist_data.loc[valid_pc_indices, 'pc']
        hist_data.loc[valid_pc_indices, 'dp'] = (hist_data.loc[valid_pc_indices, 'd'] / hist_data.loc[valid_pc_indices, 'pc']) * 100

        # Select and order columns (Added 'v' for volume, remove if not needed)
        columns_to_keep = ['ticker', 'company_name', 'date', 'o', 'h', 'l', 'c', 'v', 'pc', 'd', 'dp']
        # Filter out columns that might not exist (like 'v' if actions=True)
        df_selected = hist_data[[col for col in columns_to_keep if col in hist_data.columns]]

        # Round float columns
        float_cols = ['o', 'h', 'l', 'c', 'pc', 'd', 'dp']
        for col in float_cols:
            if col in df_selected.columns:
                # errors='coerce' turns non-numeric into NaN, which is fine for DB (NULL)
                df_selected[col] = pd.to_numeric(df_selected[col], errors='coerce').round(4)

        print(f"  Data for {symbol} successfully processed ({len(df_selected)} records).")
        return df_selected

    except Exception as e:
        print(f"  An error occurred while processing {symbol} ({company_name}): {e}")
        return None

def save_data_to_db(dataframes, db_path, table_name):
    """Saves a list of DataFrames to the SQLite database."""
    if not dataframes:
        print("No dataframes to save.")
        return 0

    full_df = pd.concat(dataframes, ignore_index=True)
    if full_df.empty:
        print("Concatenated DataFrame is empty. Nothing to save.")
        return 0

    print(f"\nConnecting to database '{db_path}' to save {len(full_df)} total records...")
    try:
        with sqlite3.connect(db_path) as conn:
            # Use 'replace' if saving all data at once after the loop
            # Use 'append' if saving in batches within the loop (needs table init first)
            # Since we concat after the loop, 'replace' is suitable here to overwrite old data.
            full_df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
            print(f"Data successfully written to table '{table_name}'.")

            # Create index after writing data
            print(f"Creating index idx_ticker_date on {table_name} (ticker, date)...")
            cursor = conn.cursor()
            cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_ticker_date ON {table_name} (ticker, date);")
            conn.commit()
            print("Index created successfully.")
            return len(full_df)

    except sqlite3.Error as e:
        print(f"Database error while saving data: {e}")
        return 0
    except Exception as e:
        print(f"An unexpected error occurred during database save: {e}")
        return 0


# --- Main Execution ---
if __name__ == "__main__":
    ticker_map, tickers = parse_company_data(companies_raw_data)

    end_dt = datetime.datetime.now()
    start_dt = end_dt - datetime.timedelta(days=YEARS_OF_DATA * 365 + 1) # +1 buffer day
    start_date_str = start_dt.strftime('%Y-%m-%d')
    end_date_str = end_dt.strftime('%Y-%m-%d')

    print(f"Fetching data from {start_date_str} to {end_date_str} using yfinance.")
    print(f"Will process {len(tickers)} tickers.")
    print(f"Data will be stored in SQLite DB: '{DB_FILENAME}', Table: '{TABLE_NAME}'")

    all_fetched_data = [] # List to hold individual DataFrames

    for i, symbol in enumerate(tickers):
        company = ticker_map.get(symbol, "N/A")
        print(f"\nProcessing ({i+1}/{len(tickers)}): {symbol} ({company})")

        df = fetch_and_prepare_data(symbol, company, start_date_str, end_date_str)

        if df is not None and not df.empty:
            all_fetched_data.append(df)

        # Optional: Save in batches (if BATCH_SIZE is set and > 0)
        # This can be useful for very large lists of tickers to free up memory
        # and save intermediate progress to DB using 'append' (requires table init first)
        # Current implementation saves all at the end using 'replace'.
        # if BATCH_SIZE > 0 and len(all_fetched_data) >= BATCH_SIZE:
        #    print(f"--- Saving batch of {len(all_fetched_data)} dataframes ---")
        #    save_data_to_db(all_fetched_data, DB_FILENAME, TABLE_NAME, if_exists='append') # Need 'append' here
        #    all_fetched_data = [] # Clear batch

        time.sleep(0.6) # Rate limit requests

    # Save any remaining data (or all data if not batching)
    if all_fetched_data:
        # print(f"--- Saving final batch of {len(all_fetched_data)} dataframes ---")
        total_saved = save_data_to_db(all_fetched_data, DB_FILENAME, TABLE_NAME) # 'replace' used here
        print(f"\nFinished processing all tickers.")
        print(f"Total records saved to database: {total_saved}")
    else:
        print("\nNo data was fetched or prepared. Database was not modified.")

    print(f"Script finished. Database '{DB_FILENAME}' should contain the fetched data.")

# --- END OF FILE fetch_and_store_prices.py ---