import pandas as pd

CSV_FILE = "btc_hourly_prices.csv"  # Update if needed

try:
    df = pd.read_csv(CSV_FILE)

    # Log column names
    print("\n📌 Column Names:", df.columns.tolist())

    # Log first 10 rows
    print("\n📊 First 10 Rows of BTC Data:\n")
    print(df.head(10).to_string(index=False))

    # Log full content (Warning: Large output may be truncated)
    print("\n📄 Full CSV Data:\n")
    print(df.to_string(index=False))

except Exception as e:
    print(f"\n❌ Error reading the CSV file: {e}")
