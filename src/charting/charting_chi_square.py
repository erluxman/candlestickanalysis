import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json


def process_data_for_whisker(data):
    """Flatten the nested JSON structure into a DataFrame for whisker plot"""
    data_rows = {}
    for sector, sector_data in data.items():
        for trend, trend_data in sector_data.items():
            for timeframe, timeframe_data in trend_data.items():
                for pattern, pattern_data in timeframe_data.items():
                    for metric, metric_data in pattern_data.items():
                        # Handle "❌" values and convert to None
                        if "_trend" in metric:
                            continue
                        criteria = metric.split("_")[0]
                        p_value = (
                            metric_data["p_value"]
                            if metric_data["p_value"] != "❌"
                            else None
                        )

                        if p_value:
                            data_rows.setdefault(trend, {})
                            data_rows[trend].setdefault(pattern, {})
                            data_rows[trend][pattern].setdefault(criteria, [])
                            current_data = data_rows[trend][pattern][criteria]
                            current_data.append(p_value)
                            data_rows[trend][pattern][criteria] = current_data

    return data_rows


def create_whisker_plot(df, output_file):
    print("printing basic plot")  # Print a message indicating the start of the plot generation

    # Generate random data for demonstration
    random_data = {
        "Criteria": np.random.choice(["High", "Low","Close"], 100),  # Generate 100 random trends
        "Pattern": np.random.choice(["Hammer", "I. Hammer", "Shooting Star","Hanging Man"], 100),  # Generate 100 random patterns
        "PValue": np.random.rand(100)  # Generate 100 random p-values
    }

    order_of_candles = ["Hammer", "I. Hammer", "Shooting Star", "Hanging Man"]

    df = pd.DataFrame(random_data)  # Create a DataFrame from the random data

    # Ensure the 'Pattern' column is ordered according to 'order_of_candles'
    df["Pattern"] = pd.Categorical(df["Pattern"], categories=order_of_candles, ordered=True)
    df = df.sort_values("Pattern")
    # Define custom colors for the trends
    trend_colors = {
        "High": "black",
        "Low": "white",
        "Close": "gray"
    }

    # Create a box plot using Plotly Express with custom colors
    fig = px.box(
        df,
        x="Pattern",
        y="PValue",
        color="Criteria",
        points=False,
        color_discrete_map=trend_colors,
    )
    fig.for_each_trace(
        lambda trace: trace.update(
            line=dict(color='grey' if trace.name == 'High' else 'black', width=1.5),  # Set border color to grey if 'High', otherwise black
            fillcolor=trace.marker.color  # Explicitly retain fill color
        ),
        selector=dict(type='box')
    )
    # Create a box plot using Plotly Express

    # fig = px.box(df, x="Pattern", y="PValue", color="Trend", points="all")

    fig.update_layout(
        title="Random Data Whisker Plot",
        xaxis_title="Pattern",
        yaxis_title="P-Value",
        dragmode=False,  # Disable drag mode
        hovermode="closest",  # Set hover mode to closest
        showlegend=True,  # Show legend
        margin=dict(l=40, r=40, t=40, b=40),  # Set margins
        xaxis=dict(fixedrange=True),  # Disable zoom on x-axis
        yaxis=dict(fixedrange=True),  # Disable zoom on y-axis
        plot_bgcolor="white",  # Set background color to white
        paper_bgcolor="white"  # Set paper background color to white
    )
    fig.write_image(
        "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/src/charting/testchart.png",
        width=1920,
        height=1080,
        scale=2,
    )
    fig.show()  # Display the plot

    # Save the plot with higher resolution
    print(f"Whisker plot saved to {output_file}")

    # pattern_order = sorted(df["Pattern"].unique())

    # fig = go.Figure()

    # for trend in df["Trend"].unique():
    #     trend_df = df[df["Trend"] == trend]
    #     fig.add_trace(
    #         go.Box(
    #             x=trend_df["Pattern"],
    #             y=trend_df["PValue"],
    #             name=trend,
    #             boxpoints=False,
    #             boxmean=True,
    #         )
    #     )

    # fig.update_layout(
    #     plot_bgcolor="white",
    #     height=600,
    #     width=1000,
    #     title_text="Candlestick Pattern P-Values Whisker Plot",
    #     xaxis_title="Candlestick Pattern",
    #     yaxis_title="P-Value",
    #     boxmode="group",
    # )

    # fig.write_html(output_file)
    # fig.show()
    # print(f"Whisker plot saved to {output_file}")


def show_chart():
    # Load your data (replace this with your actual data loading)
    path_of_file = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/data/step4_descriptive_stats/np/inferal_analysis.json"
    with open(path_of_file) as f:
        data = json.load(f)
    df = process_data_for_whisker(data)
    print("fdad")
    create_whisker_plot(df, "candlestick_whisker_plot.html")
