import yfinance as yf
import pandas as pd
import pandas_ta as ta

ticker = "AAPL"
start_date = "2020-01-01"
end_date = "2024-12-31"
df = yf.download(ticker, start=start_date, end=end_date)

# Ensure the data is correct
print("Data Sample:")
print(df.head())

# Apply the hammer pattern detection
df.ta.cdl_pattern(name="eveningstar", append=True)


# Filter and print only the dates with a hammer pattern
hammer_dates = df[df["CDL_EVENINGSTAR"] != 0]
print("\nDates with Hammer Pattern:")
print(hammer_dates)
