from pandas import read_json
from src.constants.constants import *
import json


def merge_jsons():
    # merge all the candle data into one file  and call it all_candles.json
    all_candles = []
    for candle_id, candle_name in pattern_with_names.items():
        if(candle_name == "Random'"):
            file_path = os.path.join(np_data_path_candles, "Random.json")
        else:
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
                            all_data = pattern_data[candle_name.replace("'", "")]
                            data_following_trend = [
                                item
                                for item in all_data
                                if (
                                    item.get("meta_data", {})
                                    .get("trend_past", {})
                                    .get(str(duration), {})
                                    .get("trend_present", False)
                                )
                            ]

                            hit_high_all = []
                            for item in all_data:
                                ma_future = item.get("meta_data", {}).get(
                                    "ma_future", {}
                                )
                                ma_future_high = ma_future.get("High", {})
                                ma_future_high_duration = ma_future_high.get(
                                    str(duration), {}
                                )
                                if not ma_future_high_duration:
                                    continue
                                candle_approved_from_point = (
                                    ma_future_high_duration.get(
                                        "candle_approved_from_point", False
                                    )
                                )
                                if candle_approved_from_point:
                                    hit_high_all.append(item)

                            hit_low_all = []
                            for item in all_data:
                                ma_future = item.get("meta_data", {}).get(
                                    "ma_future", {}
                                )
                                ma_future_high = ma_future.get("Low", {})
                                ma_future_high_duration = ma_future_high.get(
                                    str(duration), {}
                                )
                                if not ma_future_high_duration:
                                    continue
                                candle_approved_from_point = (
                                    ma_future_high_duration.get(
                                        "candle_approved_from_point", False
                                    )
                                )
                                if candle_approved_from_point:
                                    hit_low_all.append(item)

                            hit_close_all = []
                            for item in all_data:
                                ma_future = item.get("meta_data", {}).get(
                                    "ma_future", {}
                                )
                                ma_future_high = ma_future.get("Close", {})
                                ma_future_high_duration = ma_future_high.get(
                                    str(duration), {}
                                )
                                if not ma_future_high_duration:
                                    continue
                                candle_approved_from_point = (
                                    ma_future_high_duration.get(
                                        "candle_approved_from_point", False
                                    )
                                )
                                if candle_approved_from_point:
                                    hit_close_all.append(item)

                            hit_high_trend = [
                                item
                                for item in hit_high_all
                                if (
                                    item.get("meta_data", {})
                                    .get("trend_past", {})
                                    .get(str(duration), {})
                                    .get("trend_present", False)
                                )
                            ]

                            hit_low_trend = [
                                item
                                for item in hit_low_all
                                if (
                                    item.get("meta_data", {})
                                    .get("trend_past", {})
                                    .get(str(duration), {})
                                    .get("trend_present", False)
                                )
                            ]

                            hit_close_trend = [
                                item
                                for item in hit_close_all
                                if (
                                    item.get("meta_data", {})
                                    .get("trend_past", {})
                                    .get(str(duration), {})
                                    .get("trend_present", False)
                                )
                            ]

                            occurance_trend = len(data_following_trend)
                            all_occurance = len(all_data)
                            hit_percentage_high_trend = (
                                len(hit_high_trend) / occurance_trend * 100
                                if occurance_trend
                                else 0
                            )
                            hit_percentage_high_all = (
                                len(hit_high_all) / all_occurance * 100
                                if all_occurance
                                else 0
                            )
                            hit_percentage_low_trend = (
                                len(hit_low_trend) / occurance_trend * 100
                                if occurance_trend
                                else 0
                            )
                            hit_percentage_low_all = (
                                len(hit_low_all) / all_occurance * 100
                                if all_occurance
                                else 0
                            )
                            hit_percentage_close_trend = (
                                len(hit_close_trend) / occurance_trend * 100
                                if occurance_trend
                                else 0
                            )
                            hit_percentage_close_all = (
                                len(hit_close_all) / all_occurance * 100
                                if all_occurance
                                else 0
                            )

                            analytics[sector][trend][duration][candle_name] = {
                                "occurance_trend": occurance_trend,
                                "all_occurance": all_occurance,
                                "hit_percentage_high_trend": round(
                                    hit_percentage_high_trend, 2
                                ),
                                "hit_percentage_high_all": round(
                                    hit_percentage_high_all, 2
                                ),
                                "hit_percentage_low_trend": round(
                                    hit_percentage_low_trend, 2
                                ),
                                "hit_percentage_low_all": round(
                                    hit_percentage_low_all,
                                    2,
                                ),
                                "hit_percentage_close_trend": round(
                                    hit_percentage_close_trend, 2
                                ),
                                "hit_percentage_close_all": round(
                                    hit_percentage_close_all, 2
                                ),
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
