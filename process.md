# Process taken to collect and parse /transform data

1. Download history of all stocks in Nepali market from nepsealpha between 2019-08-22 to 2024-08-11
2. Download history of top 200 stocks from NASDAQ in diverse sector in terms of market cap from Yahoo Finance
3. Convert the data downloaded from  CSV to JSON format
4. Convert non-numeric data like "20%" in the JSON file into numeric format
5. Convert it into candle stick using  TA-Lib as pandas-ta failed to produce doji patterns for few stocks.
6. Filter only those stocks that have valid data that can compute all the candle stick patterns, discard rest of the stocks specially in Nepali market with incomplete data
7. Make the same chronological order for the data of US and Nepali Market (nepali data comes with recent on top and US data comes with oldest at top)
8. From total of 1.93 Millions stock data points (one day of a stock is one data point) we extacted 743,396 various candle stick patterns and subjected our investigation over those extracted points 
9. Categorize the candlestick instances to range of increment/decrement after it happens
10. 