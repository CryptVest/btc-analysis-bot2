import requests
import os

# Check if analysis result exists
ANALYSIS_FILE = "analysis_result.txt"

if not os.path.exists(ANALYSIS_FILE):
    print("❌ Error: analysis_result.txt not found!")
    exit(1)

# Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1346726358918889584/P_940vbYSOJx9xTNol5RwVa6b3dAFeRl9XMe-NC_KM2eUHW0bh8zk8Si9ob_ckpMZH5z"

# Load analysis result
with open(ANALYSIS_FILE, "r") as f:
    analysis_content = f.read()

# Discord message limit
MAX_LENGTH = 2000  

# Function to split long messages
def split_message(message, max_length=MAX_LENGTH):
    """Splits a long message into multiple parts under max_length characters."""
    return [message[i : i + max_length] for i in range(0, len(message), max_length)]

# Split the message
parts = split_message(analysis_content)

# Send each part separately
for i, part in enumerate(parts):
    data = {"content": f"**Daily BTC Analysis (Part {i+1}/{len(parts)})**\n{part}"}
    
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    
    if response.status_code == 204:
        print(f"✅ Part {i+1} sent successfully!")
    else:
        print(f"❌ Error sending Part {i+1}: {response.status_code}, {response.text}")
        break  # Stop if there's an error

print("🚀 All parts sent successfully!") 
