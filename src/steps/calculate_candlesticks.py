import json
import os
import pandas as pd
import talib
from src.constants.constants import *
from src.steps.calculate_manual_candles import manual_candle

# candle count 1089+1910+2225+1466  = 6690

# 760+760+759+752+760+772+772+769+770+765+763+762+760+757+758+756+762+768+761+760+768+770<- days before 24th


# 2d-mv-28 = (768+770)/2 ‎ = 769
# 2d-mv-27 = (760+768)/2 ‎ = 764
# 2d-mv-26 = (761+760)/2 ‎ = 760.5
# 2d-mv-25 = (768+761)/2 ‎ = 764.5

# 2d-mv-24 = (762+768)/2 ‎ = 765
# 2d-mv-23 = (756+762)/2‎ = 759
# 2d-mv-22 = (758+756)/2‎ = 757
# 2d-mv-21 = (757+758)/2‎ = 757.5
# 2d-mv-20 = (760+757)/2‎ = 758.5

# 4d-mv-28 = (761+760+768+770)/4‎ = 764.75

# 4d-mv-24 = (758+756+762+768)/4‎ = 761
# 4d-mv-23 = (757+758+756+762)/4‎ = 758.25
# 4d-mv-22 = (760+757+758+756)/4‎ = 757.75
# 4d-mv-21 = (762+760+757+758)/4‎ = 759.25
# 4d-mv-20 = (763+762+760+757)/4‎ = 760.5
# 4d-mv-19 = (765+763+762+760)/4‎ = 762.5

# 8d-mv-24 = (763+762+760+757+758+756+762+768)/8‎ = 760.75
# 8d-mv-23 = (765+763+762+760+757+758+756+762)/8‎ = 760.375
# 8d-mv-22 = (770+765+763+762+760+757+758+756)/8‎ = 761.375
# 8d-mv-21 = (769+770+765+763+762+760+757+758)/8‎ = 763
# 8d-mv-20 = (772+769+770+765+763+762+760+757)/8‎ = 764.75
# 8d-mv-19 = (772+772+769+770+765+763+762+760)/8‎ = 766.625
# 8d-mv-18 = (760+772+772+769+770+765+763+762)/8‎ = 766.625
# 8d-mv-17 = (752+760+772+772+769+770+765+763)/8‎ = 765.375
# 8d-mv-16 = (759+752+760+772+772+769+770+765)/8‎ = 764.875
# 8d-mv-15 = (760+759+752+760+772+772+769+770)/8‎ = 764.25
# 8d-mv-14 = (760+760+759+752+760+772+772+769)/8‎ = 763


def get_moving_avg(df, criteria, interval, index):
    if index - interval >= 0:
        return df.iloc[index - interval : index][criteria].mean()
    else:
        return None


def get_moving_avg_future(df, criteria, interval, index):
    if index + interval < len(df):
        return df.iloc[index + 1 : index + interval + 1][criteria].mean()
    else:
        return None


def is_in_desired_trend(candle_type, trend_value):
    if candle_type == "CDLHAMMER":
        return trend_value == -1
    elif candle_type == "CDLINVERTEDHAMMER":
        return trend_value == -1
    elif candle_type == "CDLHANGINGMAN":
        return trend_value == 1
    elif candle_type == "CDLSHOOTINGSTAR":
        return trend_value == 1
    elif candle_type == "random":
        return True
    else:
        return False

def predicts_up_trend(candle_type):
    if candle_type == "CDLHAMMER":
        return True
    elif candle_type == "CDLINVERTEDHAMMER":
        return True
    elif candle_type == "CDLHANGINGMAN":
        return False
    elif candle_type == "CDLSHOOTINGSTAR":
        return False
    elif candle_type == "random":
        return True
    else:
        return False

def is_candle_approved(new_value, old_value, trend):
    if old_value is None or new_value is None:
        return False
    market_increased = new_value > old_value
    market_decreased = new_value < old_value
    needs_up_trend = predicts_up_trend(trend)
    if needs_up_trend and market_increased:
        return True
    if (not needs_up_trend) and market_decreased:
        return True
    return False


def calculate_random_candle(stock, input_directory, market, count):
    file = os.path.join(input_directory, f"{stock}.json")
    stock_sector = ""
    for category, tickers in sectors_under_study.items():
        if stock in tickers:
            stock_sector = category
            break
    df = pd.read_json(file)
    dates = df["Date"].values
    patterns = manual_candle(
        candle_type="random", intensity=2, stock=stock, count=count
    )
    random_candles_lengh = len(patterns)

    return calculate_meta_data(
        patterns=patterns,
        df=df,
        stock_sector=stock_sector,
        stock=stock,
        pattern="random",
        dates=dates,
    )


def calculate_additional_data(
    pattern, stock, input_directory, output_directory, market
):
    print(f"{pattern}  for {stock} in {market} market being computed")

    # file = input_directory + stock + ".json"
    file = os.path.join(input_directory, f"{stock}.json")
    stock_sector = ""
    for category, tickers in sectors_under_study.items():
        if stock in tickers:
            stock_sector = category
            break
    df = pd.read_json(file)
    dates = df["Date"].values
    patterns = manual_candle(candle_type=pattern, intensity=2, stock=stock)
    return calculate_meta_data(
        patterns=patterns,
        df=df,
        stock_sector=stock_sector,
        stock=stock,
        pattern=pattern,
        dates=dates,
    )


def calculate_meta_data(patterns, df, stock_sector, stock, pattern, dates):
    pattern_data = []

    for index, row in patterns.iterrows():
        ma_past = {criteria: {} for criteria in all_criteria}
        ma_future = {criteria: {} for criteria in all_criteria}
        trend_past = {}
        for criteria in all_criteria:
            for interval in durations:
                if index - interval >= 0:
                    ma_past[criteria][interval] = get_moving_avg(
                        df, criteria, interval, (index)
                    )
                else:
                    ma_past[criteria][interval] = None

                if index + interval < len(df):
                    ma = get_moving_avg_future(df, criteria, interval, index)
                    percentage_change_from_past_ma = (
                        (ma - ma_past[criteria][interval]) / ma_past[criteria][interval]
                        if ma_past[criteria][interval]
                        else 0
                    )*100

                    percentage_change_from_today = (
                        (ma - df.iloc[index][criteria]) / df.iloc[index][criteria]
                        if df.iloc[index][criteria]
                        else 0
                    )*100
                    
                    percentage_change_from_past_ma = round(percentage_change_from_past_ma, 2)
                    percentage_change_from_today = round(percentage_change_from_today, 2)
                    
                    candle_approved_from_ma = is_candle_approved(ma, ma_past[criteria][interval], pattern)
                    candle_approved_from_point = is_candle_approved(df.iloc[index][criteria], ma_past[criteria][interval], pattern)

                    ma_future[criteria][interval] = {
                        "ma_value": ma,
                        "change_percent_from_past_ma": percentage_change_from_past_ma,
                        "change_percent_from_today": percentage_change_from_today,
                        "candle_approved_from_ma": candle_approved_from_ma,
                        "candle_approved_from_point": candle_approved_from_point
                    }
                else:
                    ma_future[criteria][interval] = None

                if criteria == "Close" and index - (interval * 2) >= 0:
                    mv_interval_ago = get_moving_avg(
                        df, "Close", interval, index - (interval)
                    )
                    mv_yesterday = get_moving_avg(df, "Close", interval, index)
                    trend_past[interval] = {}

                    trend_daily_threshold = 0.001  # this is used to determine how much portion the stock shall move in a day basis in order to be a up/down trend

                    if mv_interval_ago > (
                        mv_yesterday * (1 + trend_daily_threshold * interval)
                    ):
                        trend_past[interval]["value"] = -1
                    elif (
                        mv_interval_ago * (1 + trend_daily_threshold * interval)
                    ) < mv_yesterday:
                        trend_past[interval]["value"] = 1
                    else:
                        trend_past[interval]["value"] = 0

                    trend_past[interval]["data"] = {
                        "interval_ago": mv_interval_ago,
                        "yesterday": mv_yesterday,
                    }

                    trend_past[interval]["trend_present"] = is_in_desired_trend(
                        pattern, trend_past[interval]["value"]
                    )

        meta_data = {
            "ma_past": ma_past,
            "ma_future": ma_future,
            "trend_past": trend_past,
        }

        pattern_data.append(
            {
                "date": dates[index],
                "pattern": pattern_with_names[pattern],
                "stock": stock,
                "meta_data": meta_data,
                "Close": row["Close"],
                "High": row["High"],
                "Low": row["Low"],
                "sector": stock_sector,
            }
        )

    return pattern_data


def calculate_candleSticks(input_directory, output_directory, market):
    os.makedirs(output_directory, exist_ok=True)

    # fetch all the candles to calculate
    for key, value in pattern_with_names.items():
        print(f"{key} -> {value}")
        if key == "random":
            continue
        # read all files from the directory
        candle_path = os.path.join(output_directory, f"{value}.json")
        random_candle_path = os.path.join(output_directory, "random.json")

        for symbol_name in snp_500_symbols if (market == "us") else nepse_symbols:
            print(f"Calculating Candlesticks for {symbol_name}")
            patterns = calculate_additional_data(
                input_directory=input_directory,
                output_directory=output_directory,
                pattern=key,
                stock=symbol_name,
                market=market,
            )

            total_random_days_to_select = len(patterns)

            random_patterns = calculate_random_candle(
                stock=symbol_name,
                input_directory=input_directory,
                market=market,
                count=len(patterns),
            )
            append_candle_data(candle_path, patterns)
            append_candle_data(random_candle_path, random_patterns)
            # append the data to the file


def append_candle_data(candle_path, patterns):
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
