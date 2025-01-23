import os

import pandas as pd
from src.constants.constants import *


def manual_hammer(data, intensity):
    return data


def manual_shooting_star(data, intensity):
    return data


def manual_marubozu(data, intensity):
    return data


def manual_candle(candle_type, intensity, stock):
    file = os.path.join(np_data_path_normalized, f"{stock}.json")
    df = pd.read_json(file)
    if candle_type == "CDLHAMMER":
        return manual_hammer(df, intensity)
    elif candle_type == "CDLEVENINGSTAR":
        return manual_shooting_star(df, intensity)
    elif candle_type == "CDLMARUBOZU":
        return manual_marubozu(df, intensity)
    else:
        return {}
