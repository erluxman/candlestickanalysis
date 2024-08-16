import yfinance as yf
import pandas as pd
import pandas_ta as ta

# ticker = "AAPL"
# start_date = "2020-01-01"
# end_date = "2024-12-31"
# df = yf.download(ticker, start=start_date, end=end_date)

df = pd.DataFrame()  # Empty DataFrame

# Load data
df = pd.read_json(
    "/Users/laxmanbhattarai/Desktop/thesis/data/stock_data/structured/AAPL.json"
)

# Ensure the data is correct


# Apply the hammer pattern detection
df.ta.cdl_pattern(name="hammer", append=True)


# Filter and print only the dates with a hammer pattern
hammer_dates = df[df["CDL_HAMMER"] != 0]
print("\nDates with Hammer Pattern:")
# loop through hammer data and print  each item in single line
for index, row in hammer_dates.iterrows():
    print(row["Date"],row["CDL_HAMMER"], row["Open"], row["High"], row["Low"], row["Close"], row["Volume"], row["CDL_HAMMER"])
# print(hammer_dates)
