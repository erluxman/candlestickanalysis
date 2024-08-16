import os
import json


def transform_data(data):
    transformed = []
    for entry in data:
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

        print(entry)
        volume = float(volume_str)

        # Create a new entry with the transformed data
        transformed_entry = {
            "Symbol": entry.get("Symbol"),
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


def read_and_transform_json_files(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, "r") as f:
                data = json.load(f)

            # Transform data
            transformed_data = transform_data(data)

            # Save transformed data
            output_file_path = os.path.join(output_directory, filename)
            with open(output_file_path, "w") as f:
                json.dump(transformed_data, f, indent=4)
            print(f"Transformed and saved {filename}")


# Define the paths
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop/thesis")
input_directory = os.path.join(desktop_path, "stock_data")
output_directory = os.path.join(desktop_path, "stock_data/structured")

# Create the structured folder if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Read, transform, and save JSON files
read_and_transform_json_files(input_directory, output_directory)
