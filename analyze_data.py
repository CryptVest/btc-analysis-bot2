import requests
import pandas as pd
import json
import os

# Define DeepSeek API URL and fetch API key
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not API_KEY:
    print("❌ Error: API key is missing! Set it in GitHub Secrets.")
    exit(1)

# Load BTC price data
try:
    df = pd.read_csv("btc_hourly_prices.csv")
except FileNotFoundError:
    print("❌ Error: btc_hourly_prices.csv not found.")
    exit(1)

# Convert only recent data to JSON format to avoid too large input
price_data = df.tail(48).to_dict(orient="records")  # Last 48 hours only

# Define the prompt for DeepSeek
prompt = f"""
Analyze the following BTC hourly price data:
{json.dumps(price_data, indent=2)}

Trading sessions in UTC:
- Asia (00:00 - 06:00)
- London (06:00 - 12:00)
- New York (12:00 - 20:00)
- Close (20:00 - 00:00)

What to analyze:
1. Count of BULL (open > close) and BEAR (close > open) in each session.
2. Trends based on session behavior and day of the week.
3. Probability of BULL/BEAR per hour.
4. Trade recommendations for today.
5. Summary.
"""

# Prepare API request
data = {
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.7
}
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Send request to DeepSeek
response = requests.post(API_URL, headers=headers, json=data)

# Handle response
if response.status_code == 200:
    try:
        result = response.json()["choices"][0]["message"]["content"]
        
        # Save analysis result
        with open("analysis_result.txt", "w") as f:
            f.write(result)
        print("✅ Analysis saved to analysis_result.txt")
    
    except (KeyError, IndexError, json.JSONDecodeError):
        print("❌ Error: Unexpected response format:", response.text)
        exit(1)

else:
    print(f"❌ Error {response.status_code}: {response.text}")
    exit(1)
