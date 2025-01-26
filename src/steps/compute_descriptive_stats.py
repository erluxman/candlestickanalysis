from pandas import read_json
from src.constants.constants import *
import json


def merge_jsons():
    # merge all the candle data into one file  and call it all_candles.json
    all_candles = []
    for candle_id, candle_name in pattern_with_names.items():
        file_path = os.path.join(np_data_path_candles, f"{candle_name}.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                all_candles.extend(data)
            else:
                print(f"Warning: {file_path} does not contain a JSON array. Skipping.")

    with open(os.path.join(np_data_path_candles, "all_candles.json"), "w") as outfile:
        json.dump(all_candles, outfile)


bear_start = "2021-08-19"
bear_end = "2023-11-27"


def save_result(result):
    if not os.path.exists(np_data_path_descriptive_stats):
        os.makedirs(np_data_path_descriptive_stats)
    with open(
        os.path.join(np_data_path_descriptive_stats, "descriptive_stats.json"),
        "w",
    ) as outfile:
        json.dump(result, outfile)


def save_analytics(result):
    if not os.path.exists(np_data_path_descriptive_stats):
        os.makedirs(np_data_path_descriptive_stats)
    with open(
        os.path.join(np_data_path_descriptive_stats, "descriptive_anylitics.json"),
        "w",
    ) as outfile:
        json.dump(result, outfile)


def categorize_stats():
    file_path = os.path.join(np_data_path_candles, "all_candles.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

        result = {}

        for entry in data:
            date = entry.get("date")
            is_bearish = bear_start <= date <= bear_end
            trend_key = "bearish" if is_bearish else "bullish"
            sector = entry.get("sector")
            if sector not in result:
                result[sector] = {}
            if trend_key not in result[sector]:
                result[sector][trend_key] = {}

            if "patterns" not in result[sector][trend_key]:
                result[sector][trend_key]["patterns"] = {}

            pattern = entry.get("pattern")
            if pattern not in result[sector][trend_key]["patterns"]:
                result[sector][trend_key]["patterns"][pattern] = []

            result[sector][trend_key]["patterns"][pattern].append(entry)

        save_result(result)


def compute_category_analytics():
    file_path = os.path.join(np_data_path_descriptive_stats, "descriptive_stats.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        analytics = {}

        for sector, trend_data in data.items():
            analytics[sector] = {}
            for trend, patterns in trend_data.items():
                analytics[sector][trend] = {}
                for pattern, pattern_data in patterns.items():
                    for duration in durations:
                        analytics[sector][trend][duration] = {}
                        for candle_id, candle_name in pattern_with_names.items():
                            data_of_candle = pattern_data[candle_name]
                            data_following_trend = data_following_trend = [
                                item
                                for item in data_of_candle
                                if (
                                    item.get("meta_data", {})
                                    .get("trend_past", {})
                                    .get(str(duration), {})
                                    .get("trend_present", False)
                                )
                            ]

                            occurance_trend = len(data_following_trend)
                            all_occurance = len(data_of_candle)
                            hit_percentage_high_trend = 60
                            hit_percentage_high_all = 40
                            hit_percentage_low_trend = 70
                            hit_percentage_low_all = 50
                            hit_percentage_close_trend = 60
                            hit_percentage_close_all = 40

                            analytics[sector][trend][duration][candle_name] = {
                                "occurance_trend": occurance_trend,
                                "all_occurance": all_occurance,
                                "hit_percentage_high_trend": hit_percentage_high_trend,
                                "hit_percentage_high_all": hit_percentage_high_all,
                                "hit_percentage_low_trend": hit_percentage_low_trend,
                                "hit_percentage_low_all": hit_percentage_low_all,
                                "hit_percentage_close_trend": hit_percentage_close_trend,
                                "hit_percentage_close_all": hit_percentage_close_all,
                            }
            analytics[sector][trend]["commentry"] = get_analytics_commentry(
                analytics[sector][trend]
            )

        save_analytics(analytics)


def get_analytics_commentry(data):
    return "This is a commentry on the following data " + str(data)


def compute_descriptive_stats():
    merge_jsons()
    categorize_stats()
    compute_category_analytics()
