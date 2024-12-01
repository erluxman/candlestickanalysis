from src.steps.normalize_data import *
from src.steps.calculate_candlesticks import *


def prepareData():
    delete_output_directories()
    download_data()
    normalize_data()


def calculate_candleSticks():
    calculate_candleSticks_us()
    calculate_candleSticks_np()
