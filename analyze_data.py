import requests
import pandas as pd
import json
import os

# Define DeepSeek API URL and API Key
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

# Define the prompt for DeepSeek
prompt = f"""
Analyze the following BTC hourly price data from 27 Feb 2025:
{json.dumps(price_data, indent=2)}

Trading sessions in UTC:
- Asia (00:00 - 06:00)
- London (06:00 - 12:00)
- New York (12:00 - 20:00)
- Close (20:00 - 00:00)

What to analyze:
1. Count of BULL (open > close) and BEAR (close > open) for each session.
2. Trends based on session behavior and day of the week.
3. Probability of BULL/BEAR per hour since 27 Feb.
4. Recommendations if I want to trade today (pattenr based on day of the weeks + what could probably happen based on the data gathered  / analyse).
5. Summary.

Make sure each session in a day is either bull or bear.
Header format: Analysis of BTC from 27 Feb - (dd/mm of the current date)
"""

# Prepare API request
data = {
    "model": "deepseek/deepseek-r1:free",  # ✅ Updated to DeepSeek R1
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.7
}
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://yourwebsite.com",  # Optional, replace with your site URL
    "X-Title": "BTC Trading Analysis Bot"  # Optional, replace with your project title
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
