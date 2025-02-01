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
        create_whisker_plot(
            process_data_for_whisker(data),
            qualified_values={
                "Criteria": [
                    "High",
                    "Close",
                    "Low",
                ],
                "Pattern": [
                    "Shooting Star",
                    "I. Hammer",
                    "Hammer",
                ],
            },
            title="When bad returns are ignored",
            filter_function=lambda x: x <= 1,
            x="Pattern",
            y="p Value",
            color="Criteria",
        )

        create_whisker_plot(
            process_data_for_whisker(data, ignore_bad_returns=False),
            qualified_values={
                "Criteria": [
                    "High",
                    "Close",
                    "Low",
                ],
                "Pattern": [
                    "Shooting Star",
                    "I. Hammer",
                    "Hammer",
                ],
            },
            title="When bad returns considered",
            filter_function=lambda x: x <= 1,
            x="Pattern",
            y="p Value",
            color="Criteria",
        )


def write_chart_to_thesis():
    write_descriptive_charts()
    write_inferencal_charts()
