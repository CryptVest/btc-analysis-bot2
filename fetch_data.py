import requests
import pandas as pd
from datetime import datetime, timedelta

# API URL for free BTC 1H data (no API key required)
CRYPTOCOMPARE_API_URL = "https://min-api.cryptocompare.com/data/v2/histohour"

# Fetch BTC price since February 27, 2025
start_date = datetime(2025, 2, 27)
end_date = datetime.utcnow()

# Convert datetime to timestamps
start_timestamp = int(start_date.timestamp())
end_timestamp = int(end_date.timestamp())

# API parameters
params = {
    "fsym": "BTC",
    "tsym": "USD",
    "limit": 2000,  # Max records per request
    "toTs": end_timestamp
}

response = requests.get(CRYPTOCOMPARE_API_URL, params=params)

if response.status_code == 200:
    data = response.json()["Data"]["Data"]
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["time"], unit="s")
    
    # Keep only required columns
    df = df[["timestamp", "open"]].rename(columns={"open": "price"})
    
    # Save to CSV
    df.to_csv("btc_hourly_prices.csv", index=False)
    print("✅ Data saved to btc_hourly_prices.csv")
else:
    print(f"❌ Error fetching data: {response.status_code}, {response.text}")
