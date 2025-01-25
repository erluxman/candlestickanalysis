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


def categorize_candles():
    file_path = os.path.join(np_data_path_candles, "all_candles.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

        result = {
            "bullish": {
                "data": [],
            },
            "bearish": {
                "data": [],
            },
        }

        for entry in data:
            date = entry.get("date")
            is_bearish = bear_start <= date <= bear_end
            main_key = "bearish" if is_bearish else "bullish"
            sector = entry.get("sector")
            if sector not in result[main_key]:
                result[main_key][sector] = {"data": []}

            result[main_key][sector]["data"].append(entry)

        save_result(result)


def compute_descriptive_stats():
    merge_jsons()
    categorize_candles()
