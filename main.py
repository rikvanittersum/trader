from pandas_datareader import data as pdr
import yfinance as yf
import numpy as np
import pandas_ta as ta
yf.pdr_override()

def data_for_stock(start, end, stock):
    df = pdr.get_data_yahoo(stock, start=start, end=end)
    df.ta.stoch(high='high', low='low', k=14, d=3, append=True)
    return df

class Trade():
    def __init__(self, price):
        self.paidprice = price
        self.gain = 0
        self.holding_days = 0
        self.optimumsell = price * 1.02
    def sold(self, sell_price):
        self.gain = (sell_price - self.paidprice) / self.paidprice
    def sold_at_optimum(self):
        self.gain = self.optimumsell
    def add_holding_day(self):
        self.holding_days += 1


start = "2020-10-10"
end = "2022-05-04"
stock = "VT"

trades = []
bought_stock = None

def posses_stock(row):
    global bought_stock
    if bought_stock:
        if row.High >= bought_stock.optimumsell:
            trades.append(bought_stock.sold_at_optimum())
            sell_price = bought_stock.optimumsell
            bought_stock = None
            return sell_price
        return bought_stock.paidprice
    if row.buy:
        bought_stock = Trade(row.High)
        return row.High
    return 0

df= data_for_stock(stock=stock, start=start, end=end)
df.drop(['Volume', 'Open', 'Close', 'Adj Close'], 1, inplace=True)
df["%k change day before"] = df["STOCHk_14_3_3"] - df["STOCHk_14_3_3"].shift(1)

df["buy"] = (df["STOCHk_14_3_3"] > 25) & (df["STOCHk_14_3_3"].shift(1) < 35) & (df["STOCHk_14_3_3"] > df["STOCHd_14_3_3"]) & (df["%k change day before"] > 3)

df["sell"] = (df["STOCHk_14_3_3"] > 80) | (df["STOCHk_14_3_3"] < df["STOCHd_14_3_3"])
df["own_stock"] = df.apply(posses_stock, axis=1)

print(df.to_string())



