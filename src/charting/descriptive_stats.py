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


def plot_boxplots(data_rows):
    """Create matplotlib boxplots with side-by-side bullish/bearish comparison"""
    for duration, trends_data in data_rows.items():
        # Get sorted unique patterns
        patterns = sorted(
            set(
                pattern
                for trend_data in trends_data.values()
                for pattern in trend_data.keys()
            )
        )

        # Prepare data and positions
        box_data = []
        positions = []
        colors = []

        for idx, pattern in enumerate(patterns):
            # Calculate x positions for side-by-side boxes
            base_pos = idx * 2
            positions.extend([base_pos - 0.3, base_pos + 0.3])

            # Get data for both trends
            bullish_data = trends_data["bullish"].get(pattern, [])
            bearish_data = trends_data["bearish"].get(pattern, [])

            box_data.extend([bullish_data, bearish_data])
            colors.extend(
                ["#1f77b4", "#ff7f0e"]
            )  # Blue for bullish, orange for bearish

        # Create figure
        fig, ax = plt.subplots(figsize=(14, 8))

        # Create boxplots
        boxprops = dict(linewidth=1.5, facecolor="white")
        bp = ax.boxplot(
            box_data,
            positions=positions,
            widths=0.4,
            patch_artist=True,
            showfliers=False,
            boxprops=boxprops,
            medianprops=dict(color="black", linewidth=1.5),
        )

        # Color the boxes
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        # Configure axes
        ax.set_title(f"Return Rate Distribution ({duration}-Day Observation)", pad=20)
        ax.set_xlabel("Candlestick Patterns", labelpad=15)
        ax.set_ylabel("Return Rate (%)", labelpad=15)
        ax.set_ylim(-5, 5)

        # Set x-ticks at pattern centers
        ax.set_xticks(np.arange(0, len(patterns) * 2, 2))
        ax.set_xticklabels(patterns, rotation=45, ha="right")

        # Add grid and legend
        ax.yaxis.grid(True, linestyle="--", alpha=0.7)
        ax.legend(
            [bp["boxes"][0], bp["boxes"][1]],
            ["Bullish", "Bearish"],
            loc="upper right",
            framealpha=0.9,
        )

        # Adjust layout
        plt.tight_layout()
        plt.show()


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
        plot_boxplots(df)
