import pandas as pd
import pandas_datareader as pdr

from django_pandas.io import read_frame

def get_price(code):
    df = pd.read_csv(f'https://stooq.com/q/d/l/?s={code}&i=d',index_col=0)
    df.index = pd.to_datetime(df.index).tz_localize('Asia/Tokyo')
    return df

def get_price_time_designation(start, end, code):
    df = pd.read_csv(f'https://stooq.com/q/d/l/?s={code}&d1={start}&d2={end}&i=d', index_col=0)
    df.index = pd.to_datetime(df.index).tz_localize('Asia/Tokyo')
    return df

def get_price_date(start, end, code):
    pdr =pdr.stooq.StooqDailyReader(symbols='6701.jp', start='JAN-01-2010', end="JUN-26-2020").read().sort_values(by='Date',ascending=True)
    return pdr
