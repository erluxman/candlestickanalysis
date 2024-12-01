from datetime import datetime
import json
import os
import pandas as pd
from src.constants.constants import *
import yfinance as yf
import shutil

# Step 1 Donload Data from Yahoo finance


def transform_key_and_percentage_change(input_data, market):
    transformed_data = {}
    previous_close = None

    if market == "us":

        if isinstance(input_data, str):
            input_data = json.loads(input_data)

        # Sort timestamps to ensure chronological order

        for day_data in input_data:
            # Convert Unix timestamp (milliseconds) to datetime

            # Calculate percent change
            if previous_close is not None:
                percent_change = (
                    (float(day_data["Close"]) - previous_close) / previous_close
                ) * 100
                day_data["Percent Change"] = str(round(percent_change, 2))
            else:
                day_data["Percent Change"] = str(0.0)

            # Store current close price for next iteration
            previous_close = float(day_data["Close"])

            # Add to transformed data
            transformed_data[day_data["Date"]] = day_data

    else:

        for data_item in input_data:
            day_data = data_item.copy()
            date_str = day_data["Date"]
            day_data["Percent Change"] = str(day_data["Percent Change"])
            transformed_data[date_str] = day_data

            # Store current close price for next iteration

    return transformed_data


def transform_data(raw_data, market):
    data = transform_key_and_percentage_change(raw_data, market)

    transformed = []
    for entry in data.values():
        # Convert "Percent Change" from string to numeric
        # -1 if contains - else 1
        # Remove % sign and strip whitespace
        # Convert to float
        # If empty string, set to 0.0
        #

        multiplier = -1 if "-" in entry.get("Percent Change", "0") else 1

        percent_change_str = (
            entry.get("Percent Change", "0").replace("%", "").replace("-", "").strip()
        )

        percent_change = (
            float(percent_change_str) if percent_change_str else 0.0
        ) * multiplier

        volume_str = str(entry.get("Volume", "0")).replace("-", "").strip()
        # convert string to float

        volume_str = volume_str.replace(",", "")
        if volume_str == "":
            volume_str = "0"

        volume = float(volume_str)

        # Create a new entry with the transformed data
        transformed_entry = {
            "Date": entry.get("Date"),
            "Open": entry.get("Open"),
            "High": entry.get("High"),
            "Low": entry.get("Low"),
            "Close": entry.get("Close"),
            "Percent Change": percent_change,
            "Volume": volume,
        }
        transformed.append(transformed_entry)
    return transformed


def read_and_transform_json_files(input_directory, output_directory, market):
    os.makedirs(output_directory, exist_ok=True)
    for filename in os.listdir(input_directory):
        symbolName = filename.split(".")[0]
        containedInEnabledSymbols = symbolName in (
            snp_500_symbols if (market == "us") else nepse_symbols
        )
        if filename.endswith(".json") & containedInEnabledSymbols:
            file_path = os.path.join(input_directory, filename)
            with open(file_path, "r") as f:
                data = json.load(f)

            # Transform data
            transformed_data = transform_data(data, market)

            # Save transformed data
            output_file_path = os.path.join(output_directory, filename)
            output_file_path = output_file_path.replace("nepsealpha_export_price_", "")
            output_file_path = output_file_path.replace("_2019-08-22_2024-08-11", "")

            with open(output_file_path, "w") as f:
                json.dump(transformed_data, f, indent=4)
            print(f"Transformed and saved {filename}")


# Create the structured folder if it doesn't exist


def download_data_us():

    for stock in snp_500_symbols:
        # save to a json file in the data/crude/us folder

        # Download historical data
        ticker = yf.Ticker(stock)
        stock_data = ticker.history(start="2019-12-31", end="2024-11-28", interval="1d")
        stock_data.columns = stock_data.columns.to_flat_index()

        # Convert the data to JSON format with a more readable structure
        stock_data_json = stock_data.to_json(orient="index")

        # Convert the data to JSON format
        # stock_data_json = stock_data.to_json(orient="index")
        stock_dict = stock_data.reset_index().to_dict(orient="records")

        for day_data in stock_dict:
            # Convert Unix timestamp (milliseconds) to datetime
            day_data["Date"] = (day_data["Date"]).strftime("%Y-%m-%d")
            del day_data["Dividends"]
            del day_data["Stock Splits"]

        # Create filename with current timestamp
        filename = f"{stock}.json"

        # Define the file path
        file_path = os.path.join(us_data_path_crude, f"{stock}.json")

        # Save the data to a JSON file
        os.makedirs(us_data_path_crude, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(stock_dict, f, indent=4, default=str)

        print(f"Data for {stock} saved successfully.")


# Step 2 Normalize US Market Data
def normalize_data_us():
    read_and_transform_json_files(us_data_path_crude, us_data_path_normalized, "us")
    print("US data normalized")


# Step 3 Normalize Nepali Market Data
def normalize_data_np():
    read_and_transform_json_files(np_data_path_crude, np_data_path_normalized, "np")
    print("NP data normalized")


def download_data():
    download_data_us()
def delete_output_directories():
    
    shutil.rmtree(us_data_path_normalized, ignore_errors=True)
    shutil.rmtree(np_data_path_normalized, ignore_errors=True)
    shutil.rmtree(us_data_path_candles, ignore_errors=True)
    shutil.rmtree(np_data_path_candles, ignore_errors=True)
    
def normalize_data():
    normalize_data_us()
    normalize_data_np()
