from pandas import read_json
from src.constants.constants import *
import json


def compute_descriptive_stats():
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
