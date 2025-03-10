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
    analysis_content = f.read().strip()  # Trim excessive spaces/newlines

# Discord message limit (safe buffer)
MAX_LENGTH = 1900  

def format_for_discord(text):
    """Formats tables & messages for better readability in Discord."""
    lines = text.split("\n")
    formatted_lines = []
    inside_table = False

    for line in lines:
        if "|" in line:  # Detects a table row
            if not inside_table:
                formatted_lines.append("```")  # Open code block
                inside_table = True
            formatted_lines.append(line)  # Add table row
        else:
            if inside_table:
                formatted_lines.append("```")  # Close code block
                inside_table = False
            formatted_lines.append(line)  # Add normal text

    if inside_table:  # Ensures table is closed
        formatted_lines.append("```")

    return "\n".join(formatted_lines)

def split_message(text, max_length=MAX_LENGTH):
    """Splits a long message at safe points (periods, newlines) to stay under max_length."""
    parts = []
    while len(text) > max_length:
        # Find the best split point (preferably at a sentence end or newline)
        split_index = text[:max_length].rfind(".")  # Try to split at a full stop
        if split_index == -1:  
            split_index = text[:max_length].rfind("\n")  # Otherwise, try newline
        if split_index == -1:  
            split_index = max_length  # If no good split, force at max_length
        
        parts.append(text[:split_index+1].strip())  # Include the full stop
        text = text[split_index+1:].strip()  # Continue with remaining text

    if text:
        parts.append(text.strip())  # Add remaining part

    return parts

# Format content properly
formatted_content = format_for_discord(analysis_content)

# Split the message safely
parts = split_message(formatted_content)

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
