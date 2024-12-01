import yfinance as yf
import json
from datetime import datetime, timedelta

def download_apple_stock_data(start_date=None, end_date=None):
    # If no dates are provided, default to last 5 years
    if start_date is None:
        start_date = datetime.now() - timedelta(days=5 * 365)
    if end_date is None:
        end_date = datetime.now()

    # Download Apple stock data
    ticker = yf.Ticker("AAPL")

    # Fetch historical market data
    stock_data = ticker.history(
        start=start_date, end=end_date, interval="1d"  # Daily data
    )

    # Convert DataFrame to dictionary for JSON serialization
    # We'll convert the index to string to make it JSON serializable
    stock_dict = stock_data.reset_index().to_dict(orient="records")

    # Create filename with current timestamp
    filename = f"apple_stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Save to JSON file
    with open(filename, "w") as f:
        json.dump(stock_dict, f, indent=4, default=str)

    print(f"Stock data saved to {filename}")
    return filename
