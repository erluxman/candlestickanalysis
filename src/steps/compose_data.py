import json
import os
from src.constants.constants import *
import pandas as pd


def export_to_excel(input_dir, output_dir, market):
    print("Exporting data to excel")
    # read every file from the directory
    os.makedirs(output_dir, exist_ok=True)
    full_data = []
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
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


def export_summary_to_json():
    print("Exporting summary to JSON")
