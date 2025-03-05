import requests
import os

# Check if analysis result exists
ANALYSIS_FILE = "analysis_result.txt"

if not os.path.exists(ANALYSIS_FILE):
    print("❌ Error: analysis_result.txt not found!")
    exit(1)

# Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1346726358918889584/P_940vbYSOJx9xTNol5RwVa6b3dAFeRl9XMe-NC_KM2eUHW0bh8zk8Si9ob_ckpMZH5z"

# Load and clean analysis result
with open(ANALYSIS_FILE, "r", encoding="utf-8") as f:
    analysis_content = f.read().strip()  # Remove excessive spaces/newlines

# Discord message limit (set slightly lower to be safe)
MAX_LENGTH = 1990  

# Function to split message safely
def split_message(message, max_length=MAX_LENGTH):
    """Splits a long message into chunks without breaking words abruptly."""
    words = message.split(" ")
    parts = []
    part = ""

    for word in words:
        if len(part) + len(word) + 1 > max_length:  # +1 for space
            parts.append(part.strip())  # Add current part and reset
            part = word
        else:
            part += " " + word
    
    if part:
        parts.append(part.strip())

    return parts

# Split the message into safe parts
parts = split_message(analysis_content)

# Send each part separately
for i, part in enumerate(parts):
    data = {"content": f"**Daily BTC Analysis (Part {i+1}/{len(parts)})**\n{part}"}

    response = requests.post(DISCORD_WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print(f"✅ Part {i+1}/{len(parts)} sent successfully!")
    else:
        print(f"❌ Error sending Part {i+1}: {response.status_code}, {response.text}")
        break  # Stop on error

print("🚀 All parts processed!")  
