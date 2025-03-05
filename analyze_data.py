import requests
import pandas as pd
import json

# DeepSeek API details
import os

API_KEY = os.getenv("DEEPSEEK_API_KEY")
headers = {"Authorization": f"Bearer {API_KEY}"}


# Load BTC price data
df = pd.read_csv("btc_hourly_prices.csv")

# Convert data to JSON format for DeepSeek
price_data = df.to_dict(orient="records")

# Define the prompt for DeepSeek
prompt = f"""
Analyze the following BTC hourly price data:
{price_data}

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
    "model": "deepseek-coder",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.7
}
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Send request to DeepSeek
response = requests.post(API_URL, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()["choices"][0]["message"]["content"]
    
    # Save analysis result
    with open("analysis_result.txt", "w") as f:
        f.write(result)
    print("✅ Analysis saved to analysis_result.txt")
else:
    print(f"❌ Error: {response.status_code}, {response.text}")
