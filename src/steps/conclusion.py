from src.constants.constants import *

def displayAverageSummaryForCandle(candleSymbol):
    print("Average Summary for Candle: ", candleSymbol)
    
    
    
    
def printAverageSummariesForCandles():
    for symbol,name in pattern_with_names.items():
        displayAverageSummaryForCandle(symbol)