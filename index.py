from src.full_thesis_flow import *
from src.steps.conclusion import printAverageSummariesForCandles
from src.writer.thesis_writer import write_thesis

prepareData()
calculate_candleSticks()
compose_transformation_result()


write_thesis()
