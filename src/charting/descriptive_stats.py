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


import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go


def create_whisker_plot(data_rows):
    """Create whisker plots for each observation duration with side-by-side trends"""
    for duration, trends in data_rows.items():
        fig = go.Figure()
        patterns = sorted(
            {p for trend_data in trends.values() for p in trend_data.keys()}
        )

        # Create custom x-axis positions for grouping
        x_positions = []
        current_pos = 0
        pos_mapping = {}

        for pattern in patterns:
            pos_mapping[pattern] = (current_pos - 0.2, current_pos + 0.2)
            current_pos += 1

        # Add traces for each trend and pattern
        for trend in ["bullish", "bearish"]:
            for pattern in patterns:
                data = trends[trend].get(pattern, [])
                if data:  # Only add if data exists
                    fig.add_trace(
                    go.Box(
                        y=data,
                        name=f"{trend.capitalize()} {pattern}",
                        boxpoints=False,
                        xaxis="x",  # Use primary x-axis
                        offsetgroup=pattern,
                        alignmentgroup=pattern,
                        x0=pos_mapping[pattern][0 if trend == "bullish" else 1],
                        showlegend=False,  # Disable legend for each trace
                        marker_color="orange" if trend == "bullish" else "blue",
                    )
                )
                # Add a horizontal line at y=0
                fig.add_shape(
                    type="line",
                    x0=-0.5,
                    x1=len(patterns) - 0.5,
                    y0=0,
                    y1=0,
                    line=dict(color="grey", width=1, dash="dash"),
                )
        # Update layout for cleaner presentation
        fig.update_layout(
            # title=f"{duration}-Day Return Rate Distribution",
            xaxis=dict(
            tickvals=[np.mean(v) for v in pos_mapping.values()],
            ticktext=patterns,
            title=f"Candlestick Patterns {duration} Days",
            showgrid=True,
            ),
            yaxis=dict(title="Return Rate (%)", range=[-5, 5], gridcolor="lightgrey"),
            boxmode="group",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(t=40, b=60, l=40, r=40),
            height=600,
            width=1200,
            legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            itemsizing="constant",
            ),
        )

        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(
                    size=10,
                    symbol="square",
                    color="orange",
                    line=dict(
                        width=2, color="darkorange"
                    ),  # Darker border around the rectangle
                ),
                name="Bullish",
                legendgroup="bullish",
            )
        )
        # Create custom legend
        fig.add_trace(
            go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(
                size=10,
                symbol="square",
                color="blue",
                line=dict(width=2, color="darkblue")  # Darker border around the rectangle
            ),
            name="Bearish",
            legendgroup="bearish",
            )
        )

        # Update legend to show in top right
        fig.update_layout(
            legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.1,  # Adjust x to create a gap between chart and legend
            itemsizing="constant",
            )
        )

        fig.show()


# Usage example:
# plot_boxplots(processed_data)
# Assuming `data_rows` is the output from `process_return_rate_data`
# Call the function to generate plots
# duration, candle, return_rate
def show_stastical_chart():
    # Your JSON data (replace this with actual data loading if needed)
    data_path = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/data/step4_descriptive_stats/np/descriptive_stats.json"
    with open(data_path) as f:
        data = json.load(f)
        df = process_return_rate_data(data)
        create_whisker_plot(df)
