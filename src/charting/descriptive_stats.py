import pandas as pd
import plotly.graph_objects as go
import json

from src.charting.box_chart_printing import create_whisker_plot


def process_descriptive_data(data):
    """Flatten the JSON structure into a nested dictionary organized by observation_duration"""
    data_rows = []  # Structure: data_rows[observation_duration][trend][pattern] = list

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
                                data_rows.append(
                                    {
                                        "Timeframe": observation_duration,
                                        "Return Rate": observation_data,
                                        "Trend": trend,
                                        "Pattern": pattern,
                                        "Criteria": criteria,
                                        "Sector": sector,
                                    }
                                )

    output_path = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/data/step4_descriptive_stats/np/processed_return_rate_data.json"
    with open(output_path, "w") as outfile:
        json.dump(data_rows, outfile, indent=4)

    return data_rows


def read_raw_data():
    data_path = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/data/step4_descriptive_stats/np/descriptive_stats.json"
    with open(data_path) as f:
        data = json.load(f)
        return process_descriptive_data(data)


def read_processed_data():
    path_of_file = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/data/step4_descriptive_stats/np/processed_return_rate_data.json"
    with open(path_of_file) as f:
        data = json.load(f)
        return pd.DataFrame(data)


def write_descriptive_charts():

    # process_descriptive_data(read_raw_data())
    df = read_processed_data()

    create_whisker_plot(
        df,
        qualified_values={
            "Criteria": [
                "High",
                "Close",
                "Low",
            ],
            "Pattern": [
                "Hammer",
                # "Shooting Star", # just pass the fields that you want filter records with
                # "I. Hammer",
            ],
            "Sector": [
                "Banking",
                "Hydropower",
                "Finance",
            ],
        },
        title="Descriptive Stats is used",
        filter_function=lambda x: -5 <= x <= 5,
        x="Sector",
        y="Return Rate",
        color="Criteria",
        grid_gap=0.5
    )
