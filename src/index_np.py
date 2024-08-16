import os
import pandas as pd
import json

# Define the paths to the CSV and JSON folders
csv_folder_path = os.path.join(os.path.expanduser("~"), "Desktop/thesis", "nepse_data_csv")
json_folder_path = os.path.join(os.path.expanduser("~"), "Desktop/thesis", "stock_data_np")

# Create the JSON folder if it doesn't exist
os.makedirs(json_folder_path, exist_ok=True)

# List all CSV files in the directory
csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith(".csv")]


# Function to convert CSV to JSON
def convert_csv_to_json(csv_file):
    # Read the CSV file
    csv_file_path = os.path.join(csv_folder_path, csv_file)
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to JSON
    json_data = df.to_json(orient="records", indent=4)

    # Define the JSON file path
    json_file_path = os.path.join(
        json_folder_path, os.path.splitext(csv_file)[0] + ".json"
    )

    # Save the JSON data to a file
    with open(json_file_path, "w") as json_file:
        json_file.write(json_data)

    print(f"Converted {csv_file} to JSON.")


# Convert each CSV file to JSON
for csv_file in csv_files:
    convert_csv_to_json(csv_file)


# def update_key_names(directory, old_key, new_key):
#     for filename in os.listdir(directory):
#         if filename.endswith(".json"):
#             file_path = os.path.join(directory, filename)
#             with open(file_path, "r") as f:
#                 data = json.load(f)

#             # Update the key names in the JSON data
#             for item in data:
#                 if old_key in item:
#                     item[new_key] = item.pop(old_key)

#             # Save the updated JSON data back to the file
#             with open(file_path, "w") as f:
#                 json.dump(data, f, indent=4)

#             print(f"Updated {filename}")


# # Define the paths and keys
# desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
# json_folder_path = os.path.join(desktop_path, "stock_data_np")

# # Update the key names in the JSON files
# update_key_names(json_folder_path, "published_date", "date")

