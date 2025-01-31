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


def plot_boxplots(data):
    for trend, trend_data in data.items():
        for observation_duration, duration_data in trend_data.items():
            fig = go.Figure()
            for pattern, pattern_data in duration_data.items():
                df = pd.DataFrame(pattern_data)
                fig.add_trace(
                    go.Box(
                        y=df.values.flatten(),
                        name=f"{pattern} ({trend})",
                        boxmean="sd",  # Shows mean and standard deviation
                    )
                )
            fig.update_layout(
                title=f"Boxplot for {observation_duration} ({trend})",
                yaxis_title="Return Rate",
                xaxis_title="Patterns",
                boxmode='group'  # Group boxes together
            )
            fig.show()


# duration, candle, return_rate
def show_stastical_chart():
    # Your JSON data (replace this with actual data loading if needed)
    data_path = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/data/step4_descriptive_stats/np/descriptive_stats.json"
    with open(data_path) as f:
        data = json.load(f)
        df = process_return_rate_data(data)
        plot_boxplots(df)
