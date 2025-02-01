import pandas as pd
import plotly.express as px
import src.steps.docx_output.docx_writer as writer

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
        dragmode=False,  # Disable drag mode
        showlegend=True,  # Show legend
        margin=dict(t=100),  # Add extra space to the top
        plot_bgcolor="white",  # Set background color to white
        paper_bgcolor="white",  # Set paper background color to white
        font=dict(size=35),  # Increase font size by 5
        xaxis=dict(title_font=dict(size=35), tickfont=dict(size=35)),
        yaxis=dict(title_font=dict(size=35), tickfont=dict(size=35)),
        legend=dict(
            font=dict(size=35),
            itemclick=False,
            tracegroupgap=30,
            borderwidth=2,
            bordercolor="black",
        ),
    )
    fig.for_each_trace(
        lambda trace: trace.update(
            line=dict(
                color="black",
                width=1.5,
            ),  # Set border color to grey if 'High', otherwise black
            fillcolor=trace.marker.color,  # Explicitly retain fill color
        ),
        selector=dict(type="box"),
    )
    return fig


candle_colors = [
    "darkslateblue",
    "white",
    "gray",
    "green",
    "blue",
    "red",
    "yellow",
    "purple",
]


def create_whisker_plot(df, qualified_values, filter_function, x, y, color, title):

    for key, values in qualified_values.items():
        df = df[df[key].isin(values)]
        df[key] = pd.Categorical(
            df[key], categories=qualified_values[key], ordered=True
        )
    df = df.sort_values(list(qualified_values.keys()))

    df = df[df[y].apply(filter_function)]

    trend_colors = {
        value: candle_colors[i % len(candle_colors)]
        for i, value in enumerate(qualified_values[color])
    }

    fig = px.box(
        df,
        x=x,
        y=y,
        color=color,
        points=False,
        notched=True,
        color_discrete_map=trend_colors,
    )

    fig = style_chart(fig, title=title)
    save_chart(fig)
