from src.writer.thesis_writer_helper import *


def write_thesis():
    clear_thesis()
    write_dummy_thesis()
    write_candlestick_selection("4.1")
    write_sectors_under_investigation("4.2")
    write_longterm_trends("4.3")
    write_shortterm_trends("4.4")
    write_all_criteria("4.5")
    write_all_observation_durations("4.6")
    write_all_descriptive_analysis("4.7")
    write_all_inferal_analysis("4.8")
    write_conclusion("5.0")
    open_thesis()
