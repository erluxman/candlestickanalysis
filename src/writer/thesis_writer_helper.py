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


def open_thesis():
    writer.open_thesis()


def clear_thesis():
    writer.clear_thesis()
