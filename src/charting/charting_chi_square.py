import pandas as pd
import plotly.express as px
import numpy as np
import json


def process_data(data):
    """Flatten the nested JSON structure into a DataFrame"""
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

                        # Convert significant to boolean
                        if isinstance(metric_data["significant"], bool):
                            significant = metric_data["significant"]
                        else:
                            significant = metric_data["significant"].lower() == "true"

                        data_rows.append(
                            {
                                "Sector": sector,
                                "Trend": trend,
                                "Timeframe": timeframe,
                                "Pattern": pattern,
                                "Metric": metric,
                                "PValue": p_value,
                                "Significant": significant,
                            }
                        )

    df = pd.DataFrame(data_rows)
    df = df.dropna()  # Remove rows with missing p-values
    df["PValue"] = df["PValue"].astype(float)
    df = df[df["PValue"] <= 0.05]  # Filter to only include significant p-values
    return df


def create_pvalue_plot(df, output_file="candlestick_pvalue_plot.html"):
    """Create a scatter plot of p-values for candlestick patterns"""
    # Create the scatter plot
    fig = px.scatter(
        df,
        x="Pattern",
        y="PValue",
        color="Trend",
        hover_name="Metric",
        hover_data=["Trend", "Timeframe", "Sector"],
        title="Candlestick Pattern P-Values",
        labels={
            "PValue": "P-Value",
            "Pattern": "Candlestick Pattern",
            "Trend": "Market Trend",
        },
        category_orders={"Trend": ["bullish", "bearish"], "Timeframe": ["2", "4", "8"]},
    )

    # Add a significance threshold line (p=0.05)
    fig.add_hline(
        y=0.05,
        line_dash="dash",
        line_color="red",
        annotation_text="Significance Threshold (p=0.05)",
        annotation_position="bottom right",
    )

    # Update layout
    fig.update_layout(
        plot_bgcolor="white",
        xaxis_title="Candlestick Pattern",
        yaxis_title="P-Value",
        height=600,
        width=1000,
    )

    # Save and show
    fig.write_html(output_file)
    fig.show()
    print(f"P-value plot saved to {output_file}")


def show_chart():
    # Load your data (replace this with your actual data loading)
    path_of_file = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/data/step4_descriptive_stats/np/inferal_analysis.json"
    with open(path_of_file) as f:
        data = json.load(f)
    # Process data and create visualization
    df = process_data(data)
    create_pvalue_plot(df)
