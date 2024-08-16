import yfinance as yf
import talib
import pandas as pd


def printCandlePattern(pattern, stock, market):
    dir = (
        "/Users/laxmanbhattarai/Desktop/thesis/data/stock_data_np/structured/"
        if (market == "np")
        else "/Users/laxmanbhattarai/Desktop/thesis/data/stock_data/structured/"
    )

    file = dir + stock + ".json"
    df = pd.read_json(file)
    open_prices = df["Open"].values
    high_prices = df["High"].values
    low_prices = df["Low"].values
    close_prices = df["Close"].values
    pattern_function = getattr(talib, pattern)
    candle = pattern_function(open_prices, high_prices, low_prices, close_prices)
    df[pattern] = candle
    patterns = df[df[pattern] != 0]
    print(f"{pattern} patterns found on the following dates:")
    print(patterns[["Date", "Open", "High", "Low", "Close", pattern]])


printCandlePattern("CDLHAMMER", "AAPL", "en")
