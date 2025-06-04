import yfinance as yf
import pandas as pd


def get_stock_data(symbol: str, start_date_str: str, end_date_str: str):
    ticker_obj = yf.Ticker(symbol)
    hist_data = ticker_obj.history( start=start_date_str,
                                    end=end_date_str,
                                    interval="1d",
                                    auto_adjust=False
                                    )
    
    return hist_data

def transform_stock_data(df: pd.DataFrame):
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
    from stocks_app.models import StocksData
    for index, row in df.iterrows():
        existing = StocksData.objects.filter(
            ticker=symbol,
            date=row.name.date()
        ).exists()
        
        if not existing:
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
            print(f"Added data for {symbol} on {row.name.date()}")
        else:
            print(f"Data for {symbol} on {row.name.date()} already exists")

def run(symbol, start_date_str, end_date_str):
    print(f"Running ETL for stock data: {symbol} from {start_date_str} to {end_date_str}")
    df = get_stock_data(symbol, start_date_str, end_date_str)
    df_transformed = transform_stock_data(df)
    load_stock_data(df_transformed, symbol)
    print(f"Stock data for {symbol} loaded successfully.")

