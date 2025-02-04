import pandas as pd
import plotly.express as px
from src.charting.descriptive_stats import write_descriptive_charts
from src.charting.box_chart_printing import create_whisker_plot
import src.steps.docx_output.docx_writer as writer
import plotly.graph_objects as go
import numpy as np
import json


def process_data_for_whisker(data, ignore_bad_returns=True):
    """Flatten the nested JSON structure into a DataFrame for whisker plot"""
    data_rows = []
    for sector, sector_data in data.items():
        for trend, trend_data in sector_data.items():
            for timeframe, timeframe_data in trend_data.items():
                for pattern, pattern_data in timeframe_data.items():
                    for metric, metric_data in pattern_data.items():
                        # Handle "❌" values and convert to None
                        if "_trend" in metric:
                            continue
                        criteria = metric.split("_")[0].title()
                        p_value = (
                            metric_data["p_value"]
                            if metric_data["p_value"] != "❌"
                            else (None if ignore_bad_returns else 1)
                        )

                        if p_value:
                            data_rows.append(
                                {
                                    "Trend": trend,
                                    "Pattern": pattern,
                                    "Criteria": criteria,
                                    "p Value": p_value,
                                    "Timeframe": timeframe,
                                    "Sector": sector,
                                }
                            )

    return pd.DataFrame(data_rows)


def write_inferencal_charts():
    path_of_file = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/data/step4_descriptive_stats/np/inferal_analysis.json"
    with open(path_of_file) as f:
        data = json.load(f)

        # for period in ["2", "4", "8"]:
        # for critera in ["Low", "High", "Close"]:
        for trend in ["bullish", "bearish"]:
            create_whisker_plot(
                process_data_for_whisker(data),
                qualified_values={
                    "Criteria": ["High", "Low", "Close"],
                    "Pattern": [
                        "Hammer",
                        "Shooting Star",  # just pass the fields that you want filter records with
                        "I. Hammer",
                        "Hanging Man",
                    ],
                    "Trend": [trend],
                },
                # title=f"{period} Day, {critera} in {trend} p Value discard -ve return {"✅" if discarded else "❌" }",
                title=f" {trend} p Value discard -ve return discarded",
                filter_function=lambda x: 0 <= x <= 0.5,
                x="Pattern",
                y="p Value",
                color="Pattern",
                grid_gap=0.05,
            )


def write_chart_to_thesis():
    write_descriptive_charts()
    write_inferencal_charts()
