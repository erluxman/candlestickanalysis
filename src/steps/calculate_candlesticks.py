import json
import os
import pandas as pd
import talib
from src.constants.constants import *


def calculate_additional_data(
    pattern, stock, input_directory, output_directory, market
):
    print(f"{pattern}  for {stock} in {market} market being computed")

    # file = input_directory + stock + ".json"
    file = os.path.join(input_directory, f"{stock}.json")
    df = pd.read_json(file)
    open_prices = df["Open"].values
    high_prices = df["High"].values
    low_prices = df["Low"].values
    close_prices = df["Close"].values
    volume = df["Volume"].values
    dates = df["Date"].values
    pattern_function = getattr(talib, pattern)
    candle = pattern_function(open_prices, high_prices, low_prices, close_prices)
    df[pattern] = candle

    # Filter rows where pattern is detected
    patterns = df[df[pattern] != 0]

    # Prepare the data structure
    pattern_data = []

    for index, row in patterns.iterrows():
        # Calculate next day and next week close amounts and volumes
        if index + 1 < len(df):
            next_day_close = df.iloc[index + 1]["Close"]
            next_day_volume = df.iloc[index + 1]["Volume"]
        else:
            next_day_close = None
            next_day_volume = None

        if (index + 5) < len(df):
            next_week_close = df.iloc[index + 5]["Close"]
            next_week_volume = df.iloc[index + 5]["Volume"].sum()
            next_week_volume_cumulative = df.iloc[index + 1 : index + 6]["Volume"].sum()
        else:
            next_week_close = None
            next_week_volume = None
            next_week_volume_cumulative = None
        if (index - 5) > 0:
            last_week_close = df.iloc[index - 5]["Close"]
            last_week_volume = df.iloc[index - 5]["Volume"].sum()
            last_week_volume_cumulative = df.iloc[index - 6 : index - 1]["Volume"].sum()
        else:
            last_week_close = None
            last_week_volume = None
            last_week_volume_cumulative = None
        # use correct conditional to  avoid None values error

        if isinstance(last_week_close, (int, float)) != True:
            continue
        if isinstance(next_week_close, (int, float)) != True:
            continue
        # Calculate percentage changes

        next_day_change_percentage = (
            (next_day_close - row["Close"]) / row["Close"] * 100
            if next_day_close
            else None
        )
        next_day_volume_change_percentage = (
            (next_day_volume - row["Volume"]) / row["Volume"] * 100
            if (next_day_volume and row["Volume"] != 0)
            else 0
        )
        next_week_change_percentage = (
            (next_week_close - row["Close"]) / row["Close"] * 100
            if next_week_close
            else None
        )
        change_from_last_week_percentage = (
            (row["Close"] - last_week_close) / last_week_close * 100
            if last_week_close
            else None
        )
        weekly_volume_change_percentage = (
            (next_week_volume_cumulative - last_week_volume_cumulative)
            / last_week_volume_cumulative
            * 100
            if (
                last_week_volume_cumulative is not None
                and next_week_volume_cumulative is not None
                and last_week_volume_cumulative != 0
            )
            else None
        )

        pattern_data.append(
            {
                "date": dates[index],
                "pattern": pattern_with_names[pattern],
                "stock": stock,
                "close_amount": row["Close"],
                "next_day_close_amount": next_day_close,
                "next_day_change_percentage": next_day_change_percentage,
                "next_day_volume": next_day_volume,
                "next_day_volume_change_percentage": next_day_volume_change_percentage,
                "next_week_close_amount": next_week_close,
                "next_week_change_percentage": next_week_change_percentage,
                "next_week_volume": next_week_volume,
                "next_week_volume_cumulative": next_week_volume_cumulative,
                "last_week_close_amount": last_week_close,
                "change_from_last_week_percentage": change_from_last_week_percentage,
                "last_week_volume": last_week_volume,
                "last_week_volume_cumulative": last_week_volume_cumulative,
                "weekly_volume_change_percentage": weekly_volume_change_percentage,
                "market": market,
                "volume": row["Volume"],
                "Percentage Change": row["Percent Change"],
            }
        )

    return pattern_data


def calculate_candleSticks(input_directory, output_directory, market):
    os.makedirs(output_directory, exist_ok=True)

    # fetch all the candles to calculate
    for key, value in pattern_with_names.items():
        print(f"{key} -> {value}")
        # read all files from the directory
        candle_path = os.path.join(output_directory, f"{value}.json")

        for symbol_name in snp_500_symbols if (market == "us") else nepse_symbols:
            print(f"Calculating Candlesticks for {symbol_name}")
            patterns = calculate_additional_data(
                input_directory=input_directory,
                output_directory=output_directory,
                pattern=key,
                stock=symbol_name,
                market=market,
            )
            # append the data to the file
            candle_data = []

            if os.path.exists(candle_path):
                with open(candle_path, "r") as f:
                    candle_data = json.load(f)
            else:
                candle_data = []
            new_patterns = pd.DataFrame(patterns).to_dict(orient="records")

            candle_data += new_patterns

            with open(candle_path, "w") as f:
                # Convert Timestamp objects to strings
                for pattern in candle_data:
                    if "date" in pattern and isinstance(pattern["date"], pd.Timestamp):
                        pattern["date"] = pattern["date"].strftime("%Y-%m-%d")
                json.dump(candle_data, f, indent=4)


def calculate_candleSticks_us():
    print("Calculating Candlesticks for US market")
    calculate_candleSticks(us_data_path_normalized, us_data_path_candles, "us")


def calculate_candleSticks_np():
    print("Calculating Candlesticks for Nepali market")
    calculate_candleSticks(np_data_path_normalized, np_data_path_candles, "np")
