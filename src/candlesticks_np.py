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
    "/Users/laxmanbhattarai/Desktop/thesis/stock_data_np/Nepse Price Export 2019-08-11 to 2024-08-11.json"
)

# Ensure the data is correct
print("Data Sample:")
print(df.head())

# Apply the hammer pattern detection
df.ta.cdl_pattern(name="hammer", append=True)


# Filter and print only the dates with a hammer pattern
hammer_dates = df[df["CDL_HAMMER"] != 0]
print("\nDates with Hammer Pattern:")
print(hammer_dates)
