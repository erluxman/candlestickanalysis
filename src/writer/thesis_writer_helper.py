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
    for pattrn in pattern_with_names.values():
        writer.add_paragraph(
            thesis_body,
            f"{list(pattern_with_names.values()).index(pattrn) + 1}. {pattrn}",
        )
    writer.save_document(thesis_body, writer.thesis_path)


def write_sectors_under_investigation(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(
        thesis_body, f"{document_order} Sectors Under Investigation", level=1
    )
    for sector, tickers in sectors_under_study.items():
        writer.add_sub_heading(thesis_body, sector)
        writer.add_paragraph(thesis_body, "Stocks:", bold=True)
        for ticker in tickers:
            writer.add_paragraph(thesis_body, f"  - {ticker}")
    writer.save_document(thesis_body, writer.thesis_path)


def write_longterm_trends(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(
        thesis_body, f"{document_order} Longterm Trends Under Study:", level=1
    )
    for trend in long_trends:
        writer.add_paragraph(thesis_body, f"  - {trend}")
    writer.save_document(thesis_body, writer.thesis_path)


def write_shortterm_trends(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(
        thesis_body, f"{document_order} Shortterm Trends Under Study:", level=1
    )
    for trend in short_trends:
        writer.add_paragraph(thesis_body, f"  - {trend}")
    writer.save_document(thesis_body, writer.thesis_path)


def write_all_descriptive_analysis(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(thesis_body, f"{document_order} Descriptive Analysis:", level=1)
    table_no = 1
    for long_trend in long_trends:
        for sector, tickers in sectors_under_study.items():
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
    for long_trend in long_trends:
        for sector, tickers in sectors_under_study.items():
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
    for criteria in all_criteria:
        writer.add_paragraph(thesis_body, f"  - {criteria}")
    writer.save_document(thesis_body, writer.thesis_path)


def write_all_observation_durations(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(thesis_body, f"{document_order} Observation Durations:", level=1)
    for duration in observation_durations_days:
        writer.add_paragraph(thesis_body, f"  - {duration} Days")
    writer.save_document(thesis_body, writer.thesis_path)


def open_thesis():
    writer.open_thesis()


def clear_thesis():
    writer.clear_thesis()


def add_table_descriptive(doc):
    # Create a new Document
    # Add a table with appropriate rows and columns
    table = doc.add_table(rows=15, cols=10)  # 3 header rows + 12 data rows

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
        ["2 Days", "Hammer", "2310", "2310", "15", "30", "15", "30", "15", "30"],
        ["", "Shooting ✦", "1980", "1980", "25", "30", "25", "30", "25", "30"],
        ["", "Marubozu", "2150", "2150", "40", "20", "40", "20", "40", "20"],
        ["", "Random", "1850", "1850", "30", "36", "30", "36", "30", "36"],
        ["4 Days", "Hammer", "2450", "2450", "30", "35", "30", "35", "30", "35"],
        ["", "Shooting ✦", "1980", "1980", "25", "30", "25", "30", "25", "30"],
        ["", "Marubozu", "2150", "2150", "40", "20", "40", "20", "40", "20"],
        ["", "Random", "1850", "1850", "30", "36", "30", "36", "30", "36"],
        ["8 Days", "Hammer", "2750", "2750", "30", "35", "30", "35", "30", "35"],
        ["", "Shooting ✦", "1980", "1980", "25", "30", "25", "30", "25", "30"],
        ["", "Marubozu", "2150", "2150", "40", "20", "40", "20", "40", "20"],
        ["", "Random", "1850", "1850", "30", "36", "30", "36", "30", "36"],
    ]

    # Populate data
    for idx, row_data in enumerate(data):
        row_num = 3 + idx
        for col_num, value in enumerate(row_data):
            if col_num == 0 and not value:  # Skip empty Period cells
                continue
            table.cell(row_num, col_num).text = value

    # Merge Period cells properly
    for group_start in [0, 4, 8]:
        start_row = 3 + group_start
        end_row = start_row + 3
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
