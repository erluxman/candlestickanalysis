import random
import src.steps.docx_output.docx_writer as writer
from src.constants.constants import *
from docx import Document
import json
from docx.shared import Pt, RGBColor, Inches
from docx.enum.table import WD_ALIGN_VERTICAL


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
    descriptive_analysis_file = (
        f"{np_data_path_descriptive_stats}/descriptive_analytics.json"
    )
    thesis_body = writer.thesis_body()
    with open(descriptive_analysis_file, "r") as file:
        descriptive_data = json.load(file)
        writer.add_heading(
            thesis_body, f"{document_order} Descriptive Analysis:", level=1
        )
        table_no = 1
        for sector, tickers in sectors_under_study.items():
            for long_trend in long_trends:
                table_data = descriptive_data[sector][long_trend.lower()]
                writer.add_paragraph(
                    thesis_body,
                    analyze_candle_patterns(table_data, sector, long_trend, table_no),
                )
                add_table_descriptive(thesis_body, table_data)

                writer.add_paragraph(
                    thesis_body,
                    f"Table {table_no}. Candles Observation for {sector} Stocks in {long_trend} Market",
                    small_font=True,
                )
                table_no += 1
    writer.save_document(thesis_body, writer.thesis_path)


def analyze_candle_patterns(
    table_data, sector="technology", market_trend="bullish", table_no=1
):
    analysis = f"""The Table no. {table_no} examines candlestick pattern predictive capabilities in the {sector.capitalize()} sector 
during a long-term {market_trend} market. \n\n"""
    random_connective_words_negative = [
        "however",
        "on the other hand",
        "conversely",
        "in contrast",
    ]
    random_connective_words_positive = [
        "Furthermore, ",
        "Additionally, ",
        "Likewise, ",
        "Similarly, ",
        "And, ",
    ]
    stats_description = ""
    used_connectives = True
    is_positive_explanation = True
    explanations = {
        "hit_percentage_high_trend": "High criteria with trend",
        "hit_percentage_high_all": "High criteria regardless of trend",
        "hit_percentage_low_trend": "Low criteria with trend",
        "hit_percentage_low_all": "Low criteria regardless of trend",
        "hit_percentage_close_trend": "Close criteria with trend",
        "hit_percentage_close_all": "Close criteria regardless of trend",
    }
    for period, candles in table_data.items():
        if period == "commentry":
            continue
        random_performance = candles.get("Random", {})
        random_bearish_performance = candles.get("Random*", {})

        for candle, candle_data in candles.items():
            criteria_success = []
            if candle == "Random" or candle == "Random*":
                continue
            is_bullish = (
                True if (candle == "Hammer") or (candle == "I. Hammer") else False
            )
            random_to_compare = (
                random_performance if is_bullish else random_bearish_performance
            )
            for key, value in candle_data.items():
                if key not in explanations.keys():
                    continue
                random_value = random_to_compare.get(key, 0)
                candle_value = value
                if random_value + 20 < candle_value:
                    criteria_success.append(explanations[key])
            if len(criteria_success) > 0:
                if not used_connectives:
                    stats_description += random.choice(random_connective_words_positive)
                    used_connectives = True
                else:
                    connector = random.choice(random_connective_words_positive)
                    if len(stats_description) > 0:
                        stats_description += (
                            f"\n\n{connector if random.choice([True, False]) else ''}"
                        )
                        used_connectives = False
                stats_description += f"{candle.replace("I.","Inverted")} shows strong performance when {', '.join(criteria_success)} is used instead of picking stocks randomly when we want to pick and hold for {period} Days in average. "

    analysis += stats_description
    return analysis


def write_all_inferal_analysis(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(thesis_body, f"{document_order} Inferal Analysis:", level=1)
    table_no = 11

    descriptive_analysis_file = (
        f"{np_data_path_descriptive_stats}/descriptive_analytics.json"
    )
    thesis_body = writer.thesis_body()
    with open(descriptive_analysis_file, "r") as file:
        descriptive_data = json.load(file)

        for sector, tickers in sectors_under_study.items():
            for long_trend in long_trends:
                table_data = descriptive_data[sector][long_trend.lower()]
                # writer.add_paragraph(
                #     thesis_body, get_random_inferal_analysis_text(table_no)
                # )
                add_table_inferal(thesis_body, table_data, sector, long_trend)

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


def add_table_descriptive(doc, table_data):
    # Create table structure
    table = doc.add_table(rows=1, cols=10)
    table.style = "Table Grid"
    table.autofit = False
    table.allow_autofit = False

    # ===== COLUMN WIDTH CONFIGURATION =====
    column_widths = [
        Inches(0.1).emu,  # Period column
        Inches(1.1).emu,  # Widened Candles column (2 inches)
        Inches(0.5).emu,
        Inches(0.5).emu,
        Inches(0.5).emu,
        Inches(0.5).emu,
        Inches(0.5).emu,
        Inches(0.5).emu,
        Inches(0.5).emu,
        Inches(0.5).emu,
    ]

    for idx, width in enumerate(column_widths):
        col = table.columns[idx]
        col.width = width

    # ========== HEADER CONSTRUCTION ==========
    def format_header_cell(cell, text):
        cell.text = text
        paragraph = cell.paragraphs[0]
        run = paragraph.runs[0]
        run.font.size = Pt(9)
        run.font.bold = True

    # Main headers
    headers = [
        (0, 0, "Time"),
        (1, 1, "Candles"),
        (2, 3, "Occurance"),
        (4, 5, "Hit(%) HIGH"),
        (6, 7, "Hit(%) LOW"),
        (8, 9, "Hit(%) Close"),
    ]

    # Create header row
    hdr_row = table.rows[0]
    for start_col, end_col, text in headers:
        if start_col == end_col:
            format_header_cell(hdr_row.cells[start_col], text)
        else:
            merged = hdr_row.cells[start_col].merge(hdr_row.cells[end_col])
            format_header_cell(merged, text)

    # Sub-header row
    sub_hdr = table.add_row().cells
    sub_headers = [
        "",
        "",
        "Trend",
        "All",
        "Trend",
        "All",
        "Trend",
        "All",
        "Trend",
        "All",
    ]
    for col, text in enumerate(sub_headers):
        sub_hdr[col].text = text
        paragraph = sub_hdr[col].paragraphs[0]
        paragraph.runs[0].font.size = Pt(9)

    # Merge vertical headers
    for col in [0, 1]:
        main_cell = table.cell(0, col).merge(table.cell(1, col))

    # ========== DATA POPULATION ==========
    periods = sorted(
        (k for k in table_data.keys() if k.isdigit()), key=lambda x: int(x)
    )

    table_cells = []
    for period in periods:
        candles = table_data.get(period, {})
        for candle, data in candles.items():
            row = [
                f"{period}D",
                candle.replace("Inverted", "I."),
                str(data.get("occurance_trend", "")),
                str(data.get("all_occurance", "")),
                f"{data.get('hit_percentage_high_trend', 0):.1f}",
                f"{data.get('hit_percentage_high_all', 0):.1f}",
                f"{data.get('hit_percentage_low_trend', 0):.1f}",
                f"{data.get('hit_percentage_low_all', 0):.1f}",
                f"{data.get('hit_percentage_close_trend', 0):.1f}",
                f"{data.get('hit_percentage_close_all', 0):.1f}",
            ]
            table_cells.append(row)

    # Add data rows with formatting
    for row_data in table_cells:
        row_cells = table.add_row().cells
        for col_idx, value in enumerate(row_data):
            cell = row_cells[col_idx]
            cell.text = value
            cell.width = column_widths[col_idx]

            # Format percentages
            if col_idx >= 4:
                try:
                    pct_value = float(value.strip("%"))
                    run = cell.paragraphs[0].runs[0]
                    run.font.color.rgb = (
                        RGBColor(0x00, 0x88, 0x00)
                        if pct_value > 60
                        else (
                            RGBColor(0xCC, 0x00, 0x00)
                            if pct_value < 40
                            else RGBColor(0x00, 0x00, 0x00)
                        )
                    )
                    run.font.bold = pct_value > 60
                except ValueError:
                    pass

    # ========== CELL MERGING ==========
    current_row = 2  # Start after headers
    for period in periods:
        # Count rows for this period
        period_rows = sum(1 for row in table_cells if row[0] == f"{period}D")

        if period_rows > 1:
            start_cell = table.cell(current_row, 0)
            end_cell = table.cell(current_row + period_rows - 1, 0)
            merged = start_cell.merge(end_cell)
            merged.text = f"{period}D"
            merged.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        current_row += period_rows

    # Remove empty rows
    while len(table.rows) > current_row:
        table._tbl.remove(table.rows[-1]._tr)

    return doc


import json
from scipy.stats import chi2_contingency
import os


def calculate_chi_squared_tests(data):
    results = {}
    for period in data:
        period_data = data[period]
        period_results = {}
        for candle in period_data:
            if candle in ["Random", "Random*"]:
                continue
            # Determine which random counterpart to use
            if candle in ["Hammer", "I. Hammer"]:
                random_key = "Random"
            else:
                random_key = "Random*"
            if random_key not in period_data:
                continue
            candle_data = period_data[candle]
            random_data = period_data[random_key]
            candle_results = {}
            # Process each hit percentage metric
            for metric in candle_data:
                if not metric.startswith("hit_percentage_"):
                    continue
                # Determine occurrence type (trend or all)
                occurrence_type = metric.split("_")[-1]
                if occurrence_type == "trend":
                    c_occurrence = candle_data["occurance_trend"]
                    r_occurrence = random_data["occurance_trend"]
                elif occurrence_type == "all":
                    c_occurrence = candle_data["all_occurance"]
                    r_occurrence = random_data["all_occurance"]
                else:
                    continue
                # Calculate successes and failures
                c_hit = candle_data[metric]
                r_hit = random_data[metric]
                c_success = (c_occurrence * c_hit) / 100
                c_failure = c_occurrence - c_success
                r_success = (r_occurrence * r_hit) / 100
                r_failure = r_occurrence - r_success
                # Contingency table
                contingency = [[c_success, c_failure], [r_success, r_failure]]
                # Chi-squared test
                try:
                    chi2, p, _, _ = chi2_contingency(contingency)
                except:
                    chi2, p = 0.0, 1.0  # In case of error
                significant = p < 0.05
                # Extract metric part (e.g., high_trend)
                metric_part = "_".join(metric.split("_")[2:])
                candle_results[metric_part] = {
                    "chi2": chi2,
                    "p_value": p,
                    "significant": str(significant),
                }
            period_results[candle] = candle_results
        results[period] = period_results
    print(results)
    return results

from docx.oxml import parse_xml

def add_table_inferal(doc, table_data, sector, long_term_trend):
    # Generate chi-squared data
    chi_square_table = calculate_chi_squared_tests(table_data)
    # Save chi_squared_table to inferal_analysis.json
    inferal_analysis_file = f"{np_data_path_descriptive_stats}/inferal_analysis.json"
    if os.path.exists(inferal_analysis_file):
        with open(inferal_analysis_file, "r") as file:
            inferal_data = json.load(file)
    else:
        inferal_data = {}

    # Create table with dynamic sizing
    raw_data = []
    selected_table_data_raw = inferal_data[sector][long_term_trend]

    for duration, duration_data in selected_table_data_raw.items():
        for candle, candle_data in duration_data.items():
            # Format p-values with scientific notation
            def format_pval(key):
                p = candle_data[key]["p_value"]
                return f"{p:.2e}" if p < 0.001 else f"{p:.4f}"

            raw_data.append(
                [
                    f"{duration}D" if candle == "Hammer" else "",
                    candle,
                    format_pval("high_trend"),
                    format_pval("high_all"),
                    format_pval("low_trend"),
                    format_pval("low_all"),
                    format_pval("close_trend"),
                    format_pval("close_all"),
                ]
            )

    # Create table with exact needed size: 2 header rows + data rows
    num_rows = 2 + len(raw_data)
    table = doc.add_table(rows=num_rows, cols=8)
    table.style = "Table Grid"

    # ===== HEADER CONSTRUCTION =====
    # Merge header cells horizontally for p-value columns
    def merge_cells_horizontal(row, start_col, end_col):
        table.cell(row, start_col).merge(table.cell(row, end_col))

    # Merge header cells vertically for Period and Candles
    def merge_cells_vertical(col):
        cell_range = table.cell(0, col)._tc
        below_cell = table.cell(1, col)._tc
        cell_range.tcPr.append(parse_xml(f'<w:vMerge xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="restart"/>'))
        below_cell.tcPr.append(parse_xml(f'<w:vMerge xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="continue"/>'))

    # Merge Period and Candles columns vertically (first two rows)
    merge_cells_vertical(0)  # Period
    merge_cells_vertical(1)  # Candles

    # Merge p-value columns horizontally
    merge_cells_horizontal(0, 2, 3)  # P-value (HIGH)
    merge_cells_horizontal(0, 4, 5)  # P-value (LOW)
    merge_cells_horizontal(0, 6, 7)  # P-value (Close)

    # Set header texts
    table.cell(0, 0).text = "Period"
    table.cell(0, 1).text = "Candles"
    table.cell(0, 2).text = "P-value (HIGH)"
    table.cell(0, 4).text = "P-value (LOW)"
    table.cell(0, 6).text = "P-value (Close)"

    # Subheaders (only for p-value columns)
    subheaders = ["", "", "Trend", "All", "Trend", "All", "Trend", "All"]
    for col in range(2, 8):  # Start from column 2 (skip Period and Candles)
        table.cell(1, col).text = subheaders[col]

    # ===== DATA POPULATION =====
    for row_idx, row_data in enumerate(raw_data, start=2):
        # Ensure we don't exceed table bounds
        if row_idx >= num_rows:
            break

        for col_idx in range(8):
            cell = table.cell(row_idx, col_idx)
            cell.text = row_data[col_idx]

            # Format numeric cells
            if col_idx >= 2:
                try:
                    p_value = float(row_data[col_idx])
                    run = cell.paragraphs[0].runs[0]
                    run.font.color.rgb = (
                        RGBColor(0x00, 0x66, 0x00)
                        if p_value < 0.05
                        else RGBColor(0x99, 0x00, 0x00)
                    )
                except:
                    pass

    # ===== CELL MERGING =====
    current_row = 2
    while current_row < num_rows:
        if table.cell(current_row, 0).text:
            # Find how many rows to merge
            merge_count = 1
            while (
                current_row + merge_count < num_rows
                and not table.cell(current_row + merge_count, 0).text
            ):
                merge_count += 1

            if merge_count > 1:
                start = table.cell(current_row, 0)
                end = table.cell(current_row + merge_count - 1, 0)
                merged = start.merge(end)

            current_row += merge_count
        else:
            current_row += 1

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
