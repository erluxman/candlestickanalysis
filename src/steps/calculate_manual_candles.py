import os
import pandas as pd
from src.constants.constants import *


# Helper function (updated column name references)
def get_candle_components(open_price, high, low, close):
    body = abs(close - open_price)
    upper_wick = high - max(open_price, close)
    lower_wick = min(open_price, close) - low
    candle_range = high - low
    return body, upper_wick, lower_wick, candle_range


# Hammer Pattern (fixed column names)
def manual_hammer(df, intensity=2):
    hammer_values = []
    for i in range(len(df)):
        o = df["Open"].iloc[i]
        h = df["High"].iloc[i]
        l = df["Low"].iloc[i]
        c = df["Close"].iloc[i]

        body, upper_wick, lower_wick, candle_range = get_candle_components(o, h, l, c)

        is_long_lower_wick = lower_wick >= (2 * body) if body != 0 else False
        is_small_upper_wick = upper_wick <= (0.1 * candle_range)
        is_bullish = c > o
        date = df["Date"].iloc[i].strftime("%Y-%m-%d")
        if is_long_lower_wick and is_small_upper_wick and is_bullish:
            hammer_values.append(100)
        else:
            hammer_values.append(0)

    df["CDLHAMMER"] = hammer_values
    return df[df["CDLHAMMER"] != 0]


# Shooting Star (fixed column names)
def manual_shooting_star(df, intensity=2):
    shooting_star_values = []
    for i in range(len(df)):
        o = df["Open"].iloc[i]
        h = df["High"].iloc[i]
        l = df["Low"].iloc[i]
        c = df["Close"].iloc[i]

        body, upper_wick, lower_wick, candle_range = get_candle_components(o, h, l, c)

        is_long_upper_wick = upper_wick >= (2 * body) if body != 0 else False
        is_small_lower_wick = lower_wick <= (0.1 * candle_range)
        is_bearish = c < o

        if  is_long_upper_wick and is_small_lower_wick and is_bearish:
            shooting_star_values.append(-100)
        else:
            shooting_star_values.append(0)

    df["CDLSHOOTINGSTAR"] = shooting_star_values
    return df[df["CDLSHOOTINGSTAR"] != 0]


# Unified Candle Detector (fixed JSON parsing)
def manual_candle(candle_type, intensity, stock):
    file = os.path.join(np_data_path_normalized, f"{stock}.json")
    df = pd.read_json(file, orient="records")  # Critical fix here
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    if candle_type == "CDLHAMMER":
        return manual_hammer(df, intensity)
    elif candle_type == "CDLSHOOTINGSTAR":
        return manual_shooting_star(df, intensity)
    elif candle_type == "CDLMARUBOZU":
        return manual_marubozu(df, intensity)
    else:
        raise ValueError(f"Unsupported pattern: {candle_type}")
