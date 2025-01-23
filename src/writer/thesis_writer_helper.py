import src.steps.docx_output.docx_writer as writer
from src.constants.constants import *


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
    writer.add_heading(
        thesis_body, f"{document_order} Descriptive Analysis:", level=1
    )
    table_no = 1
    for long_trend in long_trends:
        for sector,tickers in sectors_under_study.items():
            writer.add_heading(
                thesis_body, f" Image for {sector} Stocks  in  {long_trend} Market"
            )
            writer.add_paragraph(
                thesis_body,
                f"Table {table_no}. Candles Observation for {sector} Stocks in {long_trend} Market",
            )
            table_no += 1
    writer.save_document(thesis_body, writer.thesis_path)


def write_all_inferal_analysis(document_order):
    thesis_body = writer.thesis_body()
    writer.add_heading(
        thesis_body, f"{document_order} Inferal Analysis:", level=1
    )
    table_no = 11
    for long_trend in long_trends:
        for sector, tickers in sectors_under_study.items():
            writer.add_heading(
                thesis_body, f" Image for {sector} Stocks  in  {long_trend} Market"
            )
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
