# Process taken to collect and parse /transform data

1. Download history of all stocks in Nepali market from nepsealpha between 2019-08-22 to 2024-08-11
2. Download history of top 200 stocks from NASDAQ in diverse sector in terms of market cap from Yahoo Finance
3. Convert the data downloaded from  CSV to JSON format
4. Convert non-numeric data like "200%" in the JSON file into numeric format
5. Convert it into candle stick using  TA-Lib as pandas-ta failed to produce doji patterns for few stocks.
6. Filter only those stocks that have valid data that can compute all the candle stick patterns, discard rest of the stocks specially in Nepali market with incomplete data
7. 