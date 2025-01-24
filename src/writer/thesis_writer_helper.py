import src.steps.docx_output.docx_writer as writer
from src.constants.constants import *
from docx import Document
from docx.shared import Pt


def write_dummy_thesis():
    writer.write_dummy_docx()


def write_candlestick_selection(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(
        thesis_body, f"{document_order} Candlestick Under investigation", level=1
    )
    writer.add_paragraph(
        thesis_body,
        "Details about candlesticks and basic information about them goes here, with their history and usage",
    )
    for pattrn in pattern_with_names.values():
        writer.add_paragraph(
            thesis_body,
            f"{list(pattern_with_names.values()).index(pattrn) + 1}. {pattrn} - details about the particular candlestick goes here",
        )
    writer.save_document(thesis_body, writer.thesis_path)


def write_sectors_under_investigation(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(
        thesis_body, f"{document_order} Sectors Under Investigation", level=1
    )
    for sector, tickers in sectors_under_study.items():
        writer.add_sub_heading(thesis_body, sector)
        writer.add_paragraph(
            thesis_body, "details about the sector and reason of selection goes here"
        )
        writer.add_paragraph(thesis_body, "Stocks:", bold=True)
        for ticker, name in tickers.items():
            writer.add_paragraph(
                thesis_body,
                f"  - {ticker} : {name} - details of the ticker and reason of selection goes here",
            )
    writer.save_document(thesis_body, writer.thesis_path)


def write_longterm_trends(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(
        thesis_body, f"{document_order} Longterm Trends Under Study:", level=1
    )
    for trend in long_trends:
        writer.add_paragraph(
            thesis_body, f"  - {trend} - details and reason of trend goes here"
        )
    writer.save_document(thesis_body, writer.thesis_path)


def write_shortterm_trends(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(
        thesis_body, f"{document_order} Shortterm Trends Under Study:", level=1
    )
    for trend in short_trends:
        writer.add_paragraph(
            thesis_body, f"  - {trend} - details of the trend goes here"
        )
    writer.save_document(thesis_body, writer.thesis_path)


def write_all_descriptive_analysis(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(thesis_body, f"{document_order} Descriptive Analysis:", level=1)
    table_no = 1
    for sector, tickers in sectors_under_study.items():
        for long_trend in long_trends:
            writer.add_paragraph(
                thesis_body, get_random_descriptive_analysis_text(table_no)
            )
            add_table_descriptive(thesis_body)

            writer.add_paragraph(
                thesis_body,
                f"Table {table_no}. Candles Observation for {sector} Stocks in {long_trend} Market",
            )
            table_no += 1
    writer.save_document(thesis_body, writer.thesis_path)


def write_all_inferal_analysis(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(thesis_body, f"{document_order} Inferal Analysis:", level=1)
    table_no = 11

    for sector, tickers in sectors_under_study.items():
        for long_trend in long_trends:
            writer.add_paragraph(
                thesis_body, get_random_inferal_analysis_text(table_no)
            )
            add_table_inferal(thesis_body)

            writer.add_paragraph(
                thesis_body,
                f"Table {table_no}. Chi-square test for {sector} Stocks  in {long_trend} Market",
            )
            table_no += 1
    writer.save_document(thesis_body, writer.thesis_path)


def write_all_criteria(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(
        thesis_body, f"{document_order} Criterias for Analysis:", level=1
    )
    writer.add_paragraph(
        thesis_body,
        "Details about selection of the following criterias goes here, and specially what is the reason behind selecting multiple criterias",
    )
    for criteria in all_criteria:
        writer.add_paragraph(thesis_body, f"  - {criteria}")
        writer.add_paragraph(
            thesis_body,
            f"Details about {criteria} goes here and its sifnificance to different candles and expeectations of observations goes here",
        )
    writer.save_document(thesis_body, writer.thesis_path)


def write_all_observation_durations(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(thesis_body, f"{document_order} Observation Durations:", level=1)
    writer.add_paragraph(
        thesis_body,
        "Details about selection of the following observation durations goes here",
    )
    for duration in durations:
        writer.add_paragraph(
            thesis_body, f"  - {duration} Days with short details (max 2-3 lines)"
        )
    writer.save_document(thesis_body, writer.thesis_path)


def write_conclusion(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(thesis_body, f"{document_order} Conclusion:", level=1)
    writer.add_heading(thesis_body, f"{document_order}.1 Summary", level=2)
    writer.add_paragraph(thesis_body, sample_summary)
    writer.add_heading(thesis_body, f"{document_order}.2 Conclusion", level=2)
    writer.add_paragraph(thesis_body, sample_conclusion)
    writer.add_heading(thesis_body, f"{document_order}.3 Recommendation", level=2)
    writer.add_paragraph(thesis_body, sample_recommendation)

    writer.save_document(thesis_body, writer.thesis_path)


def open_thesis():
    writer.open_thesis()


def clear_thesis():
    writer.clear_thesis()


def add_table_descriptive(doc):
    # Create a new Document
    # Add a table with appropriate rows and columns (now 15 data rows)
    table = doc.add_table(rows=18, cols=10)  # 3 header rows + 15 data rows

    # Set table style
    table.style = "Table Grid"

    # ========== HEADER SECTION ==========
    def merge_cells(cell1, cell2):
        cell1.merge(cell2)

    # Main headers (Period, Candles, etc.)
    table.cell(0, 0).text = "Period"
    table.cell(0, 1).text = "Candles"

    # Merge horizontal headers
    for col_range in [(2, 3), (4, 5), (6, 7), (8, 9)]:
        merge_cells(table.cell(0, col_range[0]), table.cell(0, col_range[1]))

    table.cell(0, 2).text = "Occurance"
    table.cell(0, 4).text = "Hit(%) HIGH"
    table.cell(0, 6).text = "Hit(%) LOW"
    table.cell(0, 8).text = "Hit(%) Close"

    # Sub-headers (Trend/Yes/No)
    for row in [1, 2]:
        for col in [2, 3, 4, 5, 6, 7, 8, 9]:
            table.cell(row, col).text = (
                "Trend" if row == 1 else ("YES" if col % 2 == 0 else "No")
            )

    # Merge vertical cells for Period and Candles
    for col in [0, 1]:
        for row in [0, 1]:
            merge_cells(table.cell(row, col), table.cell(row + 1, col))

    # ========== DATA SECTION ==========
    data = [
        # 2 Days Period (5 patterns)
        ["2 Days", "Hammer", "2310", "2310", "15", "30", "15", "30", "15", "30"],
        ["", "I. Hammer", "2050", "2050", "35", "25", "35", "25", "35", "25"],
        ["", "Shooting ✦", "1980", "1980", "25", "30", "25", "30", "25", "30"],
        ["", "Hanging Man", "2150", "2150", "40", "20", "40", "20", "40", "20"],
        ["", "Random", "1850", "1850", "30", "36", "30", "36", "30", "36"],
        # 4 Days Period (5 patterns)
        ["4 Days", "Hammer", "2450", "2450", "30", "35", "30", "35", "30", "35"],
        ["", "I. Hammer", "2050", "2050", "35", "25", "35", "25", "35", "25"],
        ["", "Shooting ✦", "1980", "1980", "25", "30", "25", "30", "25", "30"],
        ["", "Hanging Man", "2150", "2150", "40", "20", "40", "20", "40", "20"],
        ["", "Random", "1850", "1850", "30", "36", "30", "36", "30", "36"],
        # 8 Days Period (5 patterns)
        ["8 Days", "Hammer", "2750", "2750", "30", "35", "30", "35", "30", "35"],
        ["", "I. Hammer", "2050", "2050", "35", "25", "35", "25", "35", "25"],
        ["", "Shooting ✦", "1980", "1980", "25", "30", "25", "30", "25", "30"],
        ["", "Hanging Man", "2150", "2150", "40", "20", "40", "20", "40", "20"],
        ["", "Random", "1850", "1850", "30", "36", "30", "36", "30", "36"],
    ]

    # Populate data
    for idx, row_data in enumerate(data):
        row_num = 3 + idx
        for col_num, value in enumerate(row_data):
            if col_num == 0 and not value:  # Skip empty Period cells
                continue
            table.cell(row_num, col_num).text = value

    # Merge Period cells properly (now 5 rows per group)
    for group_start in [0, 5, 10]:  # Adjust group starts for 5-row blocks
        start_row = 3 + group_start
        end_row = start_row + 4  # Merge 5 rows (0-4, 5-9, 10-14)
        table.cell(start_row, 0).merge(table.cell(end_row, 0))

    return doc


def add_table_inferal(doc):
    # Create table with 11 rows (2 header + 9 data) and 8 columns
    # Create table with 11 rows (2 header + 9 data) and 8 columns
    table = doc.add_table(rows=11, cols=8)
    table.style = "Table Grid"

    def merge_cells(cell1, cell2):
        cell1.merge(cell2)

    # ===== HEADERS =====
    # Merge vertical headers (Period and Candles)
    merge_cells(table.cell(0, 0), table.cell(1, 0))  # Period
    merge_cells(table.cell(0, 1), table.cell(1, 1))  # Candles

    # Main headers
    table.cell(0, 0).text = "Period"
    table.cell(0, 1).text = "Candles"

    # P-value headers (merge horizontal)
    pvalue_headers = [
        (2, 3, "P-value (HIGH)"),
        (4, 5, "P-value (LOW)"),
        (6, 7, "P-value (Close)"),
    ]
    for start_col, end_col, text in pvalue_headers:
        merge_cells(table.cell(0, start_col), table.cell(0, end_col))
        table.cell(0, start_col).text = text

    # Subheaders (Yes/No)
    subheaders = ["Yes", "No", "Yes", "No", "Yes", "No"]
    for col, text in enumerate(subheaders, start=2):
        table.cell(1, col).text = text

    # ===== DATA =====
    data = [
        [
            "2 Days",
            "Hammer",
            "0.0343",
            "0.9987",
            "0.0003",
            "0.9875",
            "0.0124",
            "0.9999",
        ],
        ["", "Shooting ✦", "0.2499", "0.9987", "0.0001", "0.9567", "0.2499", "0.9995"],
        ["", "Marubozu", "0.9987", "0.0003", "0.9999", "0.0343", "0.9987", "0.0012"],
        [
            "4 Days",
            "Hammer",
            "0.1234",
            "0.9990",
            "0.0032",
            "0.9945",
            "0.0456",
            "0.9998",
        ],
        ["", "Shooting ✦", "0.2999", "0.9972", "0.0021", "0.9782", "0.1999", "0.9977"],
        ["", "Marubozu", "0.9999", "0.0009", "0.9987", "0.0213", "0.9995", "0.0045"],
        [
            "8 Days",
            "Hammer",
            "0.0678",
            "0.9954",
            "0.0054",
            "0.9899",
            "0.0789",
            "0.9993",
        ],
        ["", "Shooting ✦", "0.1999", "0.9966", "0.0019", "0.9654", "0.1776", "0.9921"],
        ["", "Marubozu", "0.9988", "0.0007", "0.9994", "0.0198", "0.9991", "0.0023"],
    ]

    # Populate data and merge period cells
    for row_idx, row_data in enumerate(data, start=2):
        # Only write Period if it's not empty
        if row_data[0]:  # First column (Period) has value
            table.cell(row_idx, 0).text = row_data[0]

        # Write other columns normally
        for col_idx in range(1, 8):
            table.cell(row_idx, col_idx).text = row_data[col_idx]

        # Merge period cells for first row of each group
        if row_data[0]:
            start_row = row_idx
            end_row = start_row + 2
            for merge_row in range(start_row + 1, end_row + 1):
                try:
                    merge_cells(table.cell(start_row, 0), table.cell(merge_row, 0))
                except:
                    # Handle case where cells are already merged
                    pass
    return doc


def get_random_descriptive_analysis_text(table_no):
    return f"""As shown in {table_no}, highlights Hit(%) values for High, Low, and Close trends across Hammer, Shooting Star, and Marubozu patterns over 2 Days, 4 Days, and 8 Days. Below are the positive combinations with meaningful results:

1. Marubozu
High: 40% Hit rate across all timeframes (2 Days, 4 Days, 8 Days) for Trend = Yes.

Low: 40% Hit rate across all timeframes for Trend = Yes.

Close: 40% Hit rate across all timeframes for Trend = Yes.

Insight: Marubozu is the most reliable pattern, consistently showing strong performance in predicting trends.

2. Hammer
High: 30% Hit rate in 4 Days and 8 Days for Trend = Yes.

Low: 30% Hit rate in 4 Days and 8 Days for Trend = Yes.

Close: 30% Hit rate in 4 Days and 8 Days for Trend = Yes.

Insight: Hammer shows moderate success, particularly in longer timeframes (4 Days, 8 Days).

3. Shooting Star
High: 25% Hit rate across all timeframes for Trend = Yes.

Low: 25% Hit rate across all timeframes for Trend = Yes.

Close: 25% Hit rate across all timeframes for Trend = Yes.

Insight: Shooting Star has limited success but may still be useful in specific contexts.

Key Takeaways
Marubozu is the top-performing pattern, with a 40% Hit rate across all metrics and timeframes.

Hammer shows moderate success, especially in 4 Days and 8 Days.

Shooting Star has the lowest Hit rates but may still provide some value in certain scenarios.

This analysis focuses only on combinations with positive results, helping traders identify the most effective patterns and timeframes."""


def get_random_inferal_analysis_text(table_no):
    return f"""As shown in {table_no},The table highlights P-values for High, Low, and Close trends across Hammer, Shooting Star, and Marubozu patterns over 2 Days, 4 Days, and 8 Days. Key insights:

Strong Significance:

Marubozu: Consistently significant across all timeframes (e.g., P = 0.9999 for Low in 2 Days).

Hammer: Significant in shorter timeframes (e.g., P = 0.0003 for Low in 2 Days).

Weak Significance:

Shooting Star: Weak trends (e.g., P = 0.9987 for High in 2 Days), making it unreliable.

Timeframe Impact:

Shorter timeframes (2 Days) show stronger trends, while significance weakens over longer periods (8 Days).

Implications:

Prioritize Marubozu for robust trends; use Hammer cautiously in short-term trading. Avoid relying on Shooting Star due to weak significance.

This summary provides actionable insights for traders while emphasizing the need for further validation of mid-range P-values."""


about_descriptive_analysis = """
Descriptive analysis is a statistical approach used to summarize and describe the main features of a dataset. It focuses on providing a clear and concise overview of the data, often using measures such as central tendency (mean, median, mode), dispersion (range, variance, standard deviation), and frequency distributions. Unlike inferential analysis, which aims to draw conclusions or make predictions, descriptive analysis simply organizes and presents the data in a meaningful way. It helps identify patterns, trends, and relationships within the data, making it easier to understand and interpret.

What Can We Find Out from the Table?
From the table provided, which includes Hit(%) values for High, Low, and Close trends across different candlestick patterns (Hammer, Shooting Star, Marubozu) and timeframes (2 Days, 4 Days, 8 Days), we can perform a descriptive analysis to uncover the following insights:

Pattern Performance:

The table reveals how often each candlestick pattern successfully predicts trends (Hit%). For example, Marubozu consistently shows a 40% Hit rate across all metrics and timeframes, making it the most reliable pattern. In contrast, Shooting Star has a lower Hit rate of 25%, indicating it is less effective.

Trend Effectiveness:

By examining the Hit(%) values for High, Low, and Close, we can determine which trends are more predictable. For instance, Marubozu has high Hit rates for all three metrics, suggesting it is effective for predicting upward, downward, and closing trends. On the other hand, Hammer shows moderate success, particularly in longer timeframes (4 Days, 8 Days).

Timeframe Impact:

The table allows us to analyze how the effectiveness of patterns changes over different timeframes. For example, Hammer shows improved Hit rates in longer timeframes (e.g., 30%–35% in 8 Days compared to 15%–30% in 2 Days), while Marubozu remains consistently strong across all timeframes.

Descriptive analysis of the table helps us understand the performance of different candlestick patterns and their effectiveness in predicting trends over various timeframes. By summarizing the data, we can identify which patterns are most reliable (Marubozu), which are moderately effective (Hammer), and which are less reliable (Shooting Star). This analysis provides actionable insights for traders, helping them make informed decisions based on the observed trends and patterns."""

about_inferal_analysis = """
Inferential analysis is a statistical method used to draw conclusions or make predictions about a population based on a sample of data. Unlike descriptive analysis, which focuses on summarizing and describing data, inferential analysis uses techniques such as hypothesis testing, confidence intervals, and P-values to infer properties of the larger dataset. It helps determine whether observed patterns or relationships in the data are statistically significant or simply due to random chance.

What Can We Find Out from the Table?
From the table with P-values for High, Low, and Close trends across different candlestick patterns (Hammer, Shooting Star, Marubozu) and timeframes (2 Days, 4 Days, 8 Days), we can perform inferential analysis to uncover the following insights:

Statistical Significance:

The P-values indicate whether the observed trends are statistically significant. For example:

Marubozu (2 Days, Low): P-value = 0.9999 (Trend = Yes) suggests a near-certainty of the trend being significant.

Hammer (2 Days, Low): P-value = 0.0003 (Trend = Yes) indicates strong statistical significance, rejecting the null hypothesis.

Shooting Star (2 Days, High): P-value = 0.9987 (Trend = No) suggests no significant trend.

Trend Reliability:

By analyzing the P-values, we can assess the reliability of each pattern in predicting trends. For instance:

Marubozu consistently shows strong significance across all timeframes, making it a robust indicator.

Hammer shows moderate significance in shorter timeframes but weakens over longer periods.

Shooting Star consistently shows weak significance, making it unreliable for trend prediction.

Timeframe Impact:

The P-values help us understand how the significance of trends changes over different timeframes. For example:

Hammer (2 Days, Close): P-value = 0.0124 (Trend = Yes) is significant, but in 8 Days, P-value = 0.0789 (Trend = Yes) becomes less significant.

Marubozu maintains strong significance across all timeframes, indicating its consistency.

Inferential analysis of the table allows us to determine the statistical significance of trends predicted by different candlestick patterns. By examining P-values, we can identify which patterns are reliable (Marubozu), which are moderately effective (Hammer), and which are unreliable (Shooting Star). This analysis provides a deeper understanding of the data, enabling traders to make data-driven decisions and prioritize patterns with strong statistical significance. It also highlights the importance of considering timeframes when evaluating trend reliability.
"""


sample_summary = """
This study aimed to evaluate the effectiveness of three candlestick patterns—Hammer, Shooting Star, and Marubozu—in predicting market trends across different timeframes (2 Days, 4 Days, 8 Days). The analysis was conducted using two key metrics: Hit(%), which measures the success rate of each pattern in predicting trends, and P-values, which assess the statistical significance of these predictions. The study focused on three primary trends: High, Low, and Close.

Descriptive Analysis
The descriptive analysis revealed clear differences in the performance of the three patterns. Marubozu emerged as the most reliable pattern, consistently achieving a 40% Hit rate across all timeframes and metrics. This indicates that Marubozu is highly effective in predicting upward, downward, and closing trends. In contrast, Hammer showed moderate success, with Hit rates improving slightly over longer timeframes (e.g., 30%–35% in 8 Days compared to 15%–30% in 2 Days). Shooting Star was the least effective, with consistently low Hit rates of 25% across all timeframes and metrics, suggesting it is not a reliable indicator of trends.

Inferential Analysis
The inferential analysis, based on P-values, provided further insights into the statistical significance of the observed trends. Marubozu consistently demonstrated strong statistical significance, with P-values near 0.9999 for Trend = Yes, indicating near-certainty in its predictions. Hammer showed moderate significance in shorter timeframes (e.g., P = 0.0003 for Low in 2 Days) but weakened over longer periods (e.g., P = 0.0789 for Close in 8 Days). Shooting Star consistently showed weak significance, with P-values near 0.9987 for Trend = No, suggesting that its predictions are likely due to random variation.

Key Insights
Marubozu is the most reliable pattern, with high Hit rates and strong statistical significance across all timeframes.

Hammer is moderately effective, particularly in shorter timeframes, but its reliability diminishes over longer periods.

Shooting Star is the least reliable, with low Hit rates and weak statistical significance.


"""

sample_conclusion = """
The findings of this study provide valuable insights into the effectiveness of different candlestick patterns in predicting market trends. Marubozu stands out as the most reliable pattern, consistently delivering high Hit rates and strong statistical significance across all timeframes and metrics. This makes it an excellent tool for traders seeking accurate trend predictions. Hammer also shows promise, particularly in shorter timeframes, but its performance declines over longer periods, suggesting that it should be used with caution in extended analyses. Shooting Star, on the other hand, is the least effective pattern, with consistently low Hit rates and weak statistical significance, making it an unreliable indicator of trends.

The study also highlights the importance of considering timeframes when analyzing candlestick patterns. Shorter timeframes (e.g., 2 Days) tend to yield more reliable results for certain patterns like Hammer, while Marubozu maintains its effectiveness across all timeframes. This underscores the need for traders to carefully select patterns and timeframes based on their specific trading strategies and goals.

Overall, the results demonstrate that Marubozu is the most robust and reliable pattern for trend prediction, while Hammer and Shooting Star have limited utility. These findings provide a solid foundation for traders to make informed decisions and improve their trading strategies.


"""

sample_recommendation = """
Based on the findings of this study, the following recommendations are proposed for traders and researchers:

1. Prioritize Marubozu Patterns
Marubozu patterns should be the primary focus for traders due to their consistently high Hit rates and strong statistical significance across all timeframes. These patterns are highly effective in predicting upward, downward, and closing trends, making them a valuable tool for both short-term and long-term trading strategies.

2. Use Hammer Patterns Cautiously
Hammer patterns can be useful for short-term trend predictions, particularly in 2-day and 4-day timeframes. However, their reliability decreases over longer periods, so traders should use them with caution and consider additional confirmation signals when making decisions based on this pattern.

3. Avoid Shooting Star Patterns
Shooting Star patterns should be avoided or used with extreme caution due to their low Hit rates and weak statistical significance. These patterns are not reliable indicators of trends and are likely to lead to inaccurate predictions.

4. Consider Timeframes Carefully
Traders should carefully consider the impact of timeframes on pattern performance. Shorter timeframes (e.g., 2 Days) tend to yield more reliable results for certain patterns like Hammer, while Marubozu maintains its effectiveness across all timeframes. Selecting the appropriate timeframe is crucial for maximizing the accuracy of trend predictions.

5. Conduct Further Research
Future studies should explore larger datasets and additional candlestick patterns to validate these findings and identify other reliable indicators. Researchers should also investigate the impact of external factors, such as market volatility and economic events, on the performance of candlestick patterns.

6. Develop Trading Strategies
Traders should develop and test trading strategies that incorporate the insights from this study. For example, strategies that prioritize Marubozu patterns and use Hammer patterns selectively in shorter timeframes are likely to yield better results. Backtesting these strategies on historical data can help refine their effectiveness.

7. Educate Traders
Educational programs and resources should emphasize the importance of understanding candlestick patterns and their performance across different timeframes. Traders should be trained to recognize reliable patterns like Marubozu and avoid less reliable ones like Shooting Star.


"""
