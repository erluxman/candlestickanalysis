import pandas as pd
import plotly.express as px
import src.steps.docx_output.docx_writer as writer
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


def save_chart(fig):
    thesis_body = writer.thesis_body()

    file_name = (
        "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/src/charting/temp.png"
    )
    fig.write_image(
        file_name,
        width=1920,
        height=1080,
        scale=2,
    )
    writer.add_image(thesis_body, file_name)
    writer.save_document(thesis_body, writer.thesis_path)


def style_chart(fig, title):
    fig.update_layout(
        title={
            "text": title,
            "x": 0.5,  # Center the title
            "xanchor": "center",
            "font": {"size": 50},
        },
        xaxis_title="Pattern",
        yaxis_title="P-Value",
        dragmode=False,  # Disable drag mode
        showlegend=True,  # Show legend
        margin=dict(t=100),  # Add extra space to the top
        plot_bgcolor="white",  # Set background color to white
        paper_bgcolor="white",  # Set paper background color to white
        font=dict(size=35),  # Increase font size by 5
        xaxis=dict(title_font=dict(size=35), tickfont=dict(size=35)),
        yaxis=dict(title_font=dict(size=35), tickfont=dict(size=35)),
        legend=dict(font=dict(size=35)),
    )
    return fig


def get_dummy_data():
    trend_colors = {"High": "black", "Low": "white", "Close": "gray"}
    candles = ["Hammer", "I. Hammer", "Shooting Star", "Hanging Man"]
    return {
        "Criteria": np.random.choice(list(trend_colors.keys()), 100),
        "Pattern": np.random.choice(candles, 100),  # Generate 100 random patterns
        "PValue": np.random.rand(100),  # Generate 100 random p-values
    }


def create_whisker_plot(df, qualified_values):

    trend_colors = {"High": "black", "Low": "white", "Close": "gray"}
    candles = ["Hammer", "I. Hammer", "Shooting Star", "Hanging Man"]
    random_data = {
        "Criteria": np.random.choice(list(trend_colors.keys()), 100),
        "Pattern": np.random.choice(candles, 100),  # Generate 100 random patterns
        "PValue": np.random.rand(100),  # Generate 100 random p-values
    }

    df = pd.DataFrame(random_data)  # Create a DataFrame from the random data
    
    for key, values in qualified_values.items():
        df = df[df[key].isin(values)]

    df["Pattern"] = pd.Categorical(df["Pattern"], categories=candles, ordered=True)
    df = df.sort_values("Pattern")

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
            line=dict(
                color="grey" if trace.name == "High" else "black",
                width=1.5,
            ),  # Set border color to grey if 'High', otherwise black
            fillcolor=trace.marker.color,  # Explicitly retain fill color
        ),
        selector=dict(type="box"),
    )

    fig = style_chart(fig, "Random Data Whisker Plot")
    save_chart(fig)


def write_chart_to_thesis():
    path_of_file = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/data/step4_descriptive_stats/np/inferal_analysis.json"
    with open(path_of_file) as f:
        data = json.load(f)
    df = process_data_for_whisker(data)
    create_whisker_plot(
        df,
        qualified_values={
            "Criteria": ["High", "Low","Close"],
            "Pattern": ["Hammer", "I. Hammer"],
        },
    )
