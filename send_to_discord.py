import requests

# Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1346726358918889584/P_940vbYSOJx9xTNol5RwVa6b3dAFeRl9XMe-NC_KM2eUHW0bh8zk8Si9ob_ckpMZH5z"

# Load analysis result
with open("analysis_result.txt", "r") as f:
    analysis_content = f.read()

# Prepare Discord message
data = {"content": f"**Daily BTC Analysis**\n{analysis_content}"}

# Send message to Discord
response = requests.post(DISCORD_WEBHOOK_URL, json=data)

if response.status_code == 204:
    print("✅ Analysis sent to Discord successfully!")
else:
    print(f"❌ Error: {response.status_code}, {response.text}")
