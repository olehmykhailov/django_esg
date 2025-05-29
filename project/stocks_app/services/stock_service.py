import yfinance as yf
import pandas as pd


def get_stock_data(symbol: str, start_date_str: str, end_date_str: str):
    """
    Fetch stock data for a given symbol and date range using yfinance.
    
    :param symbol: Stock ticker symbol (e.g., 'AAPL').
    :param start_date_str: Start date in 'YYYY-MM-DD' format.
    :param end_date_str: End date in 'YYYY-MM-DD' format.
    :return: Historical stok data as a DataFrame.
    """
    # Create a Ticker object
    ticker_obj = yf.Ticker(symbol)
    hist_data = ticker_obj.history( start=start_date_str,
                                    end=end_date_str,
                                    interval="1d",
                                    auto_adjust=False # Important for getting 'Close'
                                    )
    
    return hist_data

def transform_stock_data(df: pd.DataFrame):
    """
    Transform the stock data DataFrame to include only relevant columns.
    
    :param df: DataFrame containing stock data
    :return: Transformed DataFrame with relevant columns.
    """

    df.rename(columns={
        'Date': 'date',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume',
        'Dividends': 'dividend',
        'Stock Splits': 'split'
    }, inplace=True)
    try:
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"Error converting date: {e}")

    return df

def load_stock_data(df: pd.DataFrame, symbol: str):
    """
    Load the transformed stock data into the database.
    
    :param df: Transformed DataFrame containing stock data.
    :param symbol: Stock ticker symbol.
    """
    from stocks_app.models import StocksData
    for index, row in df.iterrows():
        StocksData.objects.create(
            ticker=symbol,
            date=row.name.date(),
            open=row['open'],
            high=row['high'],
            low=row['low'],
            close=row['close'],
            adj_close=row.get('Adj Close', None),
            volume=row.get('volume', None),
            dividend=row.get('dividend', None),
            split=row.get('split', None)
        )



def run(symbol, start_date_str, end_date_str):
    """
    Main function to run the stock data ETL process.
    """
    print(f"Running ETL for stock data: {symbol} from {start_date_str} to {end_date_str}")
    # Extract
    df = get_stock_data(symbol, start_date_str, end_date_str)
    
    # Transform
    df_transformed = transform_stock_data(df)
    

    # Load
    load_stock_data(df_transformed, symbol)

    print(f"✅ Stock data for {symbol} loaded successfully.")