import requests
import pandas as pd
import json
import os

# Define DeepSeek API URL and API Key (Replace with your new API key)
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"

if not API_KEY:
    raise ValueError("❌ Error: API key is missing!")

print(f"✅ API Key Loaded: {API_KEY[:5]}********")  # Print only first 5 chars for security

# Load BTC price data
DATA_FILE = "btc_hourly_prices.csv"

if not os.path.exists(DATA_FILE):
    raise FileNotFoundError("❌ Error: btc_hourly_prices.csv not found.")

df = pd.read_csv(DATA_FILE)

# Convert only recent data to JSON format to avoid too large input
price_data = df.tail(48).to_dict(orient="records")  # Last 48 hours only

# Define the updated prompt for DeepSeek V3
prompt = f"""
I have a CSV file containing hourly BTC price data. Please analyze starting from February 27, 2025. 
The file includes two columns:

- date (YYYY-MM-DD)
- hour (0-23, representing UTC time)
- price (closing price of BTC at that hour)

I want you to analyze BTC price action based on trading sessions and hourly trends. The trading sessions in UTC+0 are:

- Asia (00:00 - 06:00 UTC)
- London (06:00 - 12:00 UTC)
- New York (12:00 - 20:00 UTC)
- Close (20:00 - 00:00 UTC)

**Analysis Required:**

1. **Session-wise Bull/Bear Count per Day**
   - For each day, classify each session as BULL if the closing price at the end of the session is higher than its opening price. Otherwise, classify it as BEAR.
   - Count how many times each session has been BULL or BEAR from February 27, 2025, until the latest available date in the dataset.

2. **Hourly Bull/Bear Probability**
   - For each hour (00:00 to 23:00 UTC), count how often it was BULL (if the next hour’s price is higher) or BEAR (if the next hour’s price is lower).
   - Convert these counts into percentages to show the probability of each hour being BULL or BEAR.

3. **Identifying Patterns & Trends**
   - Identify if certain sessions tend to be bullish or bearish on specific days of the week.
   - Highlight any repeating patterns, such as consistent bullish/bearish behavior in a particular session or hour.

**Expected Output Format:**

**Session-wise Bull/Bear Count (Example Output)**

Session | BULL Count | BEAR Count  
---------|------------|------------  
Asia | XX | XX  
London | XX | XX  
New York | XX | XX  
Close | XX | XX  

**Hourly Bull/Bear Probability (Example Output)**

Hour (UTC) | BEAR Probability | BULL Probability  
-----------|----------------|----------------  
00:00 | 87.5% | 12.5%  
01:00 | 37.5% | 62.5%  
... | ... | ...  
22:00 | 42.9% | 57.1%  

**Key Observations (Example Insights)**
- "00:00 UTC (Asia Open) is mostly bearish (87.5%), meaning BTC tends to drop at session open."
- "16:00 UTC is the most bullish (85.7%), making it a strong entry point for long trades."
- "London session shows a mix of trends but has a strong bullish bias at 09:00 and 10:00 UTC."
"""

# Prepare API request
data = {
    "model": "deepseek/deepseek-chat-v3",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.7
}
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Send request to DeepSeek
try:
    response = requests.post(API_URL, headers=headers, json=data)
    response.raise_for_status()  # Raise error for non-200 responses
    response_json = response.json()

    # Extract response content
    result = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")

    if not result:
        raise ValueError("❌ Error: DeepSeek returned an empty response.")

    # Save analysis result
    with open("analysis_result.txt", "w") as f:
        f.write(result)
    print("✅ Analysis saved to analysis_result.txt")

except requests.exceptions.RequestException as e:
    print(f"❌ Request Error: {e}")
    exit(1)

except (KeyError, IndexError, json.JSONDecodeError) as e:
    print(f"❌ Error parsing DeepSeek response: {e}")
    print(f"Response content: {response.text}")
    exit(1)
