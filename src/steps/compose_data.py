import json
import os
from src.constants.constants import *
import pandas as pd


def export_to_excel(input_dir, output_dir, market):
    print("Exporting data to excel")
    # read every file from the directory
    os.makedirs(output_dir, exist_ok=True)
    full_data = []
    for key, value in pattern_with_names.items():
        file_path = os.path.join(input_dir, value + ".json")
        with open(file_path, "r") as f:
            data = json.load(f)

        # concat the data to the full data
        full_data += data

    # export the data to excel

    df = pd.DataFrame(full_data)
    output_file = os.path.join(output_dir, f"{market}_data.xlsx")

    df.to_excel(output_file, index=False)


def export_to_excel_us():
    print("Exporting US data to excel")
    export_to_excel(us_data_path_candles, data_path_transformed, "us")
    # read every file from the directory


def export_to_excel_np():
    print("Exporting Nepali data to excel")
    export_to_excel(np_data_path_candles, data_path_transformed, "np")


column_names = [
    "next_day_change_percentage",
    "next_day_volume_change_percentage",
    "change_from_last_week_percentage",
    "last_week_volume_cumulative",
    "next_week_change_percentage",
    "next_week_volume_cumulative",
    "weekly_volume_change_percentage",
]


def export_summary_to_json(input_dir, output_dir, market):
    print("Exporting summary to JSON")
    os.makedirs(output_dir, exist_ok=True)
    summary_data = {}
    summary_data_merged = {}
    summary_data_individual = {}

    for key, value in pattern_with_names.items():
        file_path = os.path.join(input_dir, value + ".json")
        with open(file_path, "r") as f:
            data = json.load(f)
        summary_data_merged_data = {}
        for column_name in column_names:
            summary_data_merged_data[column_name] = [item[column_name] for item in data]

        summary_data_merged[value] = summary_data_merged_data

        for item in data:
            symbol = item["stock"]
            stock_data_raw = [item for item in data if item["stock"] == symbol]
            # stock_data_raw = data.where(data["stock"] == symbol).dropna()
            symbol_data_summary = {
                "next_day_change_percentage": [
                    item["next_day_change_percentage"] for item in stock_data_raw
                ],
                "next_week_change_percentage": [
                    item["next_week_change_percentage"] for item in stock_data_raw
                ],
            }
            if value not in summary_data_individual:
                summary_data_individual[value] = {}

            summary_data_individual[value][symbol] = symbol_data_summary

    summary_data["individual_trends"] = summary_data_individual
    summary_data["merged_trends"] = summary_data_merged

    output_file = os.path.join(output_dir, f"{market}_summary.json")
    with open(output_file, "w") as f:
        json.dump(summary_data, f, indent=4)


def export_summary_to_json_us():
    print("Exporting US summary to JSON")
    export_summary_to_json(us_data_path_candles, data_path_transformed, "us")


def export_summary_to_json_np():
    print("Exporting Nepali summary to JSON")
    export_summary_to_json(np_data_path_candles, data_path_transformed, "np")
