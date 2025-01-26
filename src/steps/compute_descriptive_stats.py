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

        for trend, data in data.items():
            analytics[trend] = {}
            for sector, sector_data in data.items():
                analytics[trend][sector] = {}
                sector_analytics = {}
                for pattern, pattern_data in sector_data["patterns"].items():
                    for duration in durations:
                        analytics[trend][sector][duration] = {}
                        for candle_id, candle_name in pattern_with_names.items():
                            occurance_trend = 100
                            all_occurance = 190
                            hit_percentage_high_trend = 60
                            hit_percentage_high_all = 40
                            hit_percentage_low_trend = 70
                            hit_percentage_low_all = 50
                            hit_percentage_close_trend = 60
                            hit_percentage_close_all = 40

                            analytics[trend][sector][duration][candle_name] = {
                                "occurance_trend": occurance_trend,
                                "all_occurance": all_occurance,
                                "hit_percentage_high_trend": hit_percentage_high_trend,
                                "hit_percentage_high_all": hit_percentage_high_all,
                                "hit_percentage_low_trend": hit_percentage_low_trend,
                                "hit_percentage_low_all": hit_percentage_low_all,
                                "hit_percentage_close_trend": hit_percentage_close_trend,
                                "hit_percentage_close_all": hit_percentage_close_all,
                            }

        save_analytics(analytics)


def compute_descriptive_stats():
    merge_jsons()
    categorize_stats()
    # compute_category_analytics()
