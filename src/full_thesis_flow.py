from src.steps.normalize_data import *
from src.steps.calculate_candlesticks import *
from src.steps.compose_data import *


def prepareData():
    # delete_output_directories()
    download_data()
    normalize_data()


def calculate_candleSticks():
    calculate_candleSticks_us()
    # calculate_candleSticks_np()

def compose_transformation_result():
    export_to_excel_us()
    # export_to_excel_np()
    export_summary_to_json_us()
    # export_summary_to_json_np()
    
