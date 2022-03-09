from pandas_datareader import data as pdr
import yfinance as yf
import numpy as np
import pandas_ta as ta
yf.pdr_override()


def data_for_stock(start, end, stock):
    df = pdr.get_data_yahoo(stock, start=start, end=end)
    df.ta.stoch(high='high', low='low', k=14, d=3, append=True)
    return df

start = "2021-10-10"
end = "2022-01-30"
stock = "INTC"

df= data_for_stock(stock=stock, start=start, end=end)
df.drop(['Volume', 'Open', 'Close', 'Adj Close'], 1, inplace=True)
df["%d change day before"] = df["STOCHd_14_3_3"] - df["STOCHd_14_3_3"].shift(1)
df["%k change day before"] = df["STOCHk_14_3_3"] - df["STOCHk_14_3_3"].shift(1)
print(df.to_string())
class Trend_tracker:
    def __init__(self, df):
        self.df = df

    def above_positive_level(self, row):
        row["STOCHk_14_3_3"] > 32

    def above_percent_d(self, row):
        row["STOCHk_14_3_3"] > row["STOCHd_14_3_3"]
