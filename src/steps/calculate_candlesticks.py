import json
import os
import pandas as pd
import talib
from src.constants.constants import *
from src.steps.calculate_manual_candles import manual_candle

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
    else:
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
        # Calculate next day and next week close amounts and volumes
        # if index + 1 < len(df):
        #     next_day_close = df.iloc[index + 1]["Close"]
        #     next_day_volume = df.iloc[index + 1]["Volume"]
        # else:
        #     next_day_close = None
        #     next_day_volume = None

        # if (index + 5) < len(df):
        #     next_week_close = df.iloc[index + 5]["Close"]
        #     next_week_volume = df.iloc[index + 5]["Volume"].sum()
        #     next_week_volume_cumulative = df.iloc[index + 1 : index + 6]["Volume"].sum()
        # else:
        #     next_week_close = None
        #     next_week_volume = None
        #     next_week_volume_cumulative = None
        # if (index - 5) > 0:
        #     last_week_close = df.iloc[index - 5]["Close"]
        #     last_week_volume = df.iloc[index - 5]["Volume"].sum()
        #     last_week_volume_cumulative = df.iloc[index - 6 : index - 1]["Volume"].sum()
        # else:
        #     last_week_close = None
        #     last_week_volume = None
        #     last_week_volume_cumulative = None
        # # use correct conditional to  avoid None values error

        # if isinstance(last_week_close, (int, float)) != True:
        #     continue
        # if isinstance(next_week_close, (int, float)) != True:
        #     continue
        # # Calculate percentage changes

        # next_day_change_percentage = (
        #     (next_day_close - row["Close"]) / row["Close"] * 100
        #     if next_day_close
        #     else None
        # )
        # next_day_volume_change_percentage = (
        #     (next_day_volume - row["Volume"]) / row["Volume"] * 100
        #     if (next_day_volume and row["Volume"] != 0)
        #     else 0
        # )
        # next_week_change_percentage = (
        #     (next_week_close - row["Close"]) / row["Close"] * 100
        #     if next_week_close
        #     else None
        # )
        # change_from_last_week_percentage = (
        #     (row["Close"] - last_week_close) / last_week_close * 100
        #     if last_week_close
        #     else None
        # )
        # weekly_volume_change_percentage = (
        #     (next_week_volume_cumulative - last_week_volume_cumulative)
        #     / last_week_volume_cumulative
        #     * 100
        #     if (
        #         last_week_volume_cumulative is not None
        #         and next_week_volume_cumulative is not None
        #         and last_week_volume_cumulative != 0
        #     )
        #     else None
        # )
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
                    ma_future[criteria][interval] = get_moving_avg_future(
                        df, criteria, interval, index
                    )
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

                    # moving_avgs_past = []
                    # moving_avgs_past.append(get_moving_avg(df, "Close", interval, (index-1-interval)))

                    # for i in range((index-1-interval), (index - 1)):
                    #     temp_ma = get_moving_avg(df, "Close", interval, i)
                    #     moving_avgs_past.append(temp_ma)

                    # increasing_trend_count = 0
                    # decreasing_trend_count = 0
                    # trend_past[interval] = {}
                    # trend_past[interval]["past_mas"] = moving_avgs_past
                    # for i in range(1, len(moving_avgs_past)):
                    #     if moving_avgs_past[i] > moving_avgs_past[i - 1]:
                    #         increasing_trend_count += 1
                    #     elif moving_avgs_past[i] < moving_avgs_past[i - 1]:
                    #         decreasing_trend_count += 1

                    # if increasing_trend_count / (len(moving_avgs_past)-1) >= 0.7:
                    #     trend_past[interval]["value"] = 1
                    # elif decreasing_trend_count / (len(moving_avgs_past) - 1) >= 0.7:
                    #     trend_past[interval]["value"] = -1
                    # else:
                    #     trend_past[interval]["value"] = 0

        meta_data = {
            "ma_past": ma_past,
            "ma_future": ma_future,
            "trend_past": trend_past,
        }

        # now what we need to do is Moving average of each criteria in row . moving average of Close is row["Close"] for last interval days
        # and moving average of High is row["High"] for last interval days and so on
        # and we will do interval days moving average of each criteria for each row before and after the row.
        # for example if interval is 2 days and criteria is Close then we will calculate moving average of Close for 2 days before and 2 days after the row
        # and we will do this for each criteria and for each interval
        # sample_meta_data = {
        #     "ma_past": {
        #         {
        #             "High": {"2": 23, "4": 24, "8": 25},
        #             "Low": {"2": 26, "4": 27, "8": 28},
        #             "Close": {"2": 29, "4": 30, "8": 31},
        #             "Trend": {"2": -1, "4": 1, "8": -1},
        #         }
        #     },
        #     "ma_future": {
        #         {
        #             "High": {"2": 32, "4": 33, "8": 34},
        #             "Low": {"2": 35, "4": 36, "8": 37},
        #             "Close": {"2": 38, "4": 39, "8": 40},
        #             "Trend": {"2": 1, "4": 1, "8": 1},
        #         }
        #     },
        # }

        # and add this as meta_data into one dictionary and append this dictionary to pattern_data

        pattern_data.append(
            {
                "date": dates[index],
                "pattern": pattern_with_names[pattern],
                "stock": stock,
                "meta_data": meta_data,
                "close_amount": row["Close"],
                "sector": stock_sector,
                # "next_day_close_amount": next_day_close,
                # "next_day_change_percentage": next_day_change_percentage,
                # "next_day_volume": next_day_volume,
                # "next_day_volume_change_percentage": next_day_volume_change_percentage,
                # "next_week_close_amount": next_week_close,
                # "next_week_change_percentage": next_week_change_percentage,
                # "next_week_volume": next_week_volume,
                # "next_week_volume_cumulative": next_week_volume_cumulative,
                # "last_week_close_amount": last_week_close,
                # "change_from_last_week_percentage": change_from_last_week_percentage,
                # "last_week_volume": last_week_volume,
                # "last_week_volume_cumulative": last_week_volume_cumulative,
                # "weekly_volume_change_percentage": weekly_volume_change_percentage,
                # "market": market,
                # "volume": row["Volume"],
                # "Percentage Change": row["Percent Change"],
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


def append_candle_data(candle_path, candle_data):
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
