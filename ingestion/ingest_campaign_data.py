# Establish the Source Path

# import Python built-in path-handling tool
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# MVP source file
SOURCE_FILE = PROJECT_ROOT / "data" / "raw" / "marketing_campaign_2024.csv"


print(f"Project root: {PROJECT_ROOT}")
print(f"Source file: {SOURCE_FILE}")
print(f"Source exists: {SOURCE_FILE.exists()}")



# INstect source CSV
import csv


# Inspect source CSV
with open(SOURCE_FILE, "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)

    columns = next(reader)
    row_count = sum(1 for _ in reader)


print(f"Column count: {len(columns)}")
print(f"Columns: {columns}")
print(f"Row count: {row_count}")



# Inspect Connection of Python & Duckdb
import duckdb

DATABASE_FILE = PROJECT_ROOT / "marketing_analytics.duckdb"

conn = duckdb.connect(DATABASE_FILE)

print("DuckDB connection successful.")

# conn.close() # disabled because we will use the connection below to create a table and load data into it




# Connect to DuckDB and create a table for the marketing campaign data



# Start: conn
# conn = duckdb.connect(DATABASE_FILE) # disabled because already connected above

# print("DuckDB connection successful.")

conn.execute("CREATE SCHEMA IF NOT EXISTS raw")

conn.execute("""
    CREATE OR REPLACE TABLE raw.marketing_campaign_2024 AS
    SELECT *
    FROM read_csv_auto(?)
""", [str(SOURCE_FILE)])

print("CSV loaded into DuckDB.")




# Original at this point to th top, the rest are added for me to remind where i put it



# Validate loaded row count
row_count = conn.execute("""
    SELECT COUNT(*)
    FROM raw.marketing_campaign_2024
""").fetchone()[0]

print(f"DuckDB row count: {row_count}")


# Validate loaded columns
column_count = conn.execute("""
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = 'raw'
      AND table_name = 'marketing_campaign_2024'
""").fetchone()[0]

print(f"DuckDB column count: {column_count}")


# Inspect first record
first_row = conn.execute("""
    SELECT *
    FROM raw.marketing_campaign_2024
    LIMIT 1
""").fetchone()

print(f"First row: {first_row}")



# end: conn
conn.close()


