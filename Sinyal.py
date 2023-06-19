import requests
import pandas as pd
import numpy as np


endpoint = "https://api.binance.com/api/v3/klines"
symbol = str(input('Coin adını gir (BTCUSDT) : '))
interval = str(input('Kaç dakikalık/saatlik mumlar ile çalışsın (5m, 1h): '))


response = requests.get(endpoint, params={"symbol": symbol, "interval": interval})
data = response.json()
data = [d for d in data]


df = pd.DataFrame(data, columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
df["Open"] = df["Open"].astype(float)
df["High"] = df["High"].astype(float)
df["Low"] = df["Low"].astype(float)
df["Close"] = df["Close"].astype(float)
df["Volume"] = df["Volume"].astype(float)
df["Close time"] = pd.to_datetime(df["Close time"], unit="ms")
df["Quote asset volume"] = df["Quote asset volume"].astype(float)
df["Number of trades"] = df["Number of trades"].astype(int)
df["Taker buy base asset volume"] = df["Taker buy base asset volume"].astype(float)
df["Taker buy quote asset volume"] = df["Taker buy quote asset volume"].astype(float)


ema_26 = df["Close"].ewm(span=26).mean()


ema_12 = df["Close"].ewm(span=12).mean()


macd = ema_12 - ema_26


signal = macd.ewm(span=9).mean()


histogram = macd - signal


df["Buy"] = np.where((macd > 0) & (signal > 0) & (macd > signal), True, False)
df["Sell"] = np.where((macd < 0) & (signal < 0) & (macd < signal), True, False)


df.to_csv("strategy.csv")


print(df[["Open time", "Close", "Buy", "Sell"]])
