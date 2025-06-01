import pandas as pd


def calc_yearly_avg_stock(df):
    return df.groupby('year')['close'].mean().reset_index().rename(columns={'close': 'avg_close_price'})

def merge_indicator_with_stock(indicator_df, indicator_col, stock_df):
    stock_avg = calc_yearly_avg_stock(stock_df)
    merged = pd.merge(indicator_df[['year', indicator_col]], stock_avg, on='year')
    return merged