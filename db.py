import sqlite3
import pandas as pd

DATABASE = "stocks.db"
CSV_FILE = "stocks.csv"  # Update this with your actual CSV filename

# Load CSV into DataFrame
df = pd.read_csv(CSV_FILE)

# Ensure correct column names exist
required_columns = {"Symbol", "Date", "Close", "EMA_10", "EMA_20"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"CSV file must have columns: {required_columns}")

# Convert Date column to proper format
df["Date"] = pd.to_datetime(df["Date"])

# Connect to SQLite
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Symbol TEXT,
        Date TEXT,
        Close REAL,
        EMA_10 REAL,
        EMA_20 REAL
    )
""")

# Insert data into SQLite (replace if exists)
df.to_sql("stocks", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("✅ Data successfully loaded into SQLite!")
