import pandas as pd
import plotly.graph_objects as go
import json


def process_return_rate_data(data):
    """Flatten the JSON structure into a nested dictionary organized by observation_duration"""
    data_rows = {}  # Structure: data_rows[observation_duration][trend][pattern] = list

    for sector, sector_data in data.items():
        for trend, trend_data in sector_data.items():
            for timeframe, timeframe_data in trend_data.items():
                for pattern, pattern_data in timeframe_data.items():
                    if pattern == "Random":
                        continue
                    for metric in pattern_data:
                        meta_summary = metric["meta_summary"]
                        for criteria, criteria_data in meta_summary.items():
                            for (
                                observation_duration,
                                observation_data,
                            ) in criteria_data.items():
                                # Initialize nested structure
                                data_rows.setdefault(observation_duration, {})
                                data_rows[observation_duration].setdefault(trend, {})
                                data_rows[observation_duration][trend].setdefault(
                                    pattern, []
                                )

                                # Add data if exists
                                if observation_data:
                                    data_rows[observation_duration][trend][
                                        pattern
                                    ].append(observation_data)

    # Save and return the reorganized data
    output_path = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/data/step4_descriptive_stats/np/processed_return_rate_data.json"
    with open(output_path, "w") as outfile:
        json.dump(data_rows, outfile, indent=4)

    return data_rows


import matplotlib.pyplot as plt


def plot_boxplots(data_rows):
    # Iterate over each observation duration to create a separate boxplot
    for observation_duration, trends_data in data_rows.items():
        box_data = []  # List to hold data for each box (trend-pattern pair)
        labels = []  # List to hold labels for each box

        # Sort trends and patterns to ensure consistent order across plots
        for trend in sorted(trends_data.keys()):
            patterns = trends_data[trend]
            for pattern in sorted(patterns.keys()):
                data = patterns[pattern]
                if data:  # Only include if there is data
                    box_data.append(data)
                    labels.append(f"{trend}\n{pattern}")  # Newline for readability

        # Create the boxplot
        plt.figure(figsize=(14, 8))
        plt.boxplot(box_data, patch_artist=True)

        # Customize the plot
        plt.title(
            f"Return Rate Distribution (Observation Duration: {observation_duration})"
        )
        plt.xlabel("Trend and Pattern Combinations")
        plt.ylabel("Return Rate")
        plt.ylim(top=5)  # Set the maximum value for the y-axis to 5
        plt.ylim(bottom=-5)  # Set the maximum value for the y-axis to 5
        plt.xticks(range(1, len(labels) + 1), labels, rotation=45, ha="right")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()


# Assuming `data_rows` is the output from `process_return_rate_data`
# Call the function to generate plots
# duration, candle, return_rate
def show_stastical_chart():
    # Your JSON data (replace this with actual data loading if needed)
    data_path = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/data/step4_descriptive_stats/np/descriptive_stats.json"
    with open(data_path) as f:
        data = json.load(f)
        df = process_return_rate_data(data)
        plot_boxplots(df)
