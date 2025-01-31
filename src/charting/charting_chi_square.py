import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json


def process_data_for_whisker(data):
    """Flatten the nested JSON structure into a DataFrame for whisker plot"""
    data_rows = []
    for sector, sector_data in data.items():
        for trend, trend_data in sector_data.items():
            for timeframe, timeframe_data in trend_data.items():
                for pattern, pattern_data in timeframe_data.items():
                    for metric, metric_data in pattern_data.items():
                        # Handle "❌" values and convert to None
                        p_value = (
                            metric_data["p_value"]
                            if metric_data["p_value"] != "❌"
                            else None
                        )

                        data_rows.append(
                            {
                                "Sector": sector,
                                "Trend": trend,
                                "Timeframe": timeframe,
                                "Pattern": pattern,
                                "PValue": p_value,
                            }
                        )

    df = pd.DataFrame(data_rows)
    df = df.dropna()  # Remove rows with missing p-values
    df["PValue"] = df["PValue"].astype(float)
    return df

def create_whisker_plot(df, output_file):
    """Create a whisker plot for candlestick patterns"""
    # Define the order for the patterns
    pattern_order = sorted(df["Pattern"].unique())

    # Create the box plot
    fig = go.Figure()

    for trend in df["Trend"].unique():
        trend_df = df[df["Trend"] == trend]
        fig.add_trace(
            go.Box(
                x=trend_df["Pattern"],
                y=trend_df["PValue"],
                name=trend,
                boxpoints=False,
                boxmean=True,
            )
        )

    # Update layout
    fig.update_layout(
        plot_bgcolor="white",
        height=600,
        width=1000,
        title_text="Candlestick Pattern P-Values Whisker Plot",
        xaxis_title="Candlestick Pattern",
        yaxis_title="P-Value",
        boxmode="group"
    )

    # Save and show
    fig.write_html(output_file)
    fig.show()
    print(f"Whisker plot saved to {output_file}")


def show_chart():
    # Load your data (replace this with your actual data loading)
    path_of_file = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/data/step4_descriptive_stats/np/inferal_analysis.json"
    with open(path_of_file) as f:
        data = json.load(f)
    df = process_data_for_whisker(data)
    create_whisker_plot(df, "candlestick_whisker_plot.html")
