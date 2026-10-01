# Establish the Source Path

# import Python built-in path-handling tool
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# MVP source file
# SOURCE_FILE = PROJECT_ROOT / "data" / "raw" / "marketing_campaign_2024.csv"
SOURCE_FILE = sorted(
    (PROJECT_ROOT / "data" / "raw").glob("marketing_campaign_*.csv")
)



print(f"Project root: {PROJECT_ROOT}")
print(f"Source file found: {len(SOURCE_FILE)}")

for source_file in SOURCE_FILE:
    print(f" - {source_file}")



# INstect source CSV
import csv


# Inspect source CSV files
for source_file in SOURCE_FILE:
    with open(source_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        columns = next(reader)
        row_count = sum(1 for _ in reader)

    print(f"\nSource file: {source_file.name}")
    print(f"Column count: {len(columns)}")
    print(f"Columns: {columns}")
    print(f"Row count: {row_count}")



# Inspect Connection of Python & Duckdb
import duckdb

DATABASE_FILE = PROJECT_ROOT / "marketing_analytics.duckdb"

# Start: conn (new)
conn = duckdb.connect(DATABASE_FILE)

print("DuckDB connection successful.")

# conn.close() # disabled because we will use the connection below to create a table and load data into it




# Connect to DuckDB and create a table for the marketing campaign data



# Start: conn (old)
# conn = duckdb.connect(DATABASE_FILE) # disabled because already connected above

# print("DuckDB connection successful.")

conn.execute("CREATE SCHEMA IF NOT EXISTS raw")

SOURCE_PATTERN = PROJECT_ROOT / "data" / "raw" / "marketing_campaign_*.csv"

conn.execute("""
    CREATE OR REPLACE TABLE raw.marketing_campaign AS
    SELECT *
    FROM read_csv_auto(?)
""", [str(SOURCE_PATTERN)])

print("CSV loaded into DuckDB.")




# Original at this point to th top, the rest are added for me to remind where i put it



# Validate loaded row count
row_count = conn.execute("""
    SELECT COUNT(*)
    FROM raw.marketing_campaign
""").fetchone()[0]

print(f"DuckDB row count: {row_count}")


# Validate loaded columns
column_count = conn.execute("""
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = 'raw'
      AND table_name = 'marketing_campaign'
""").fetchone()[0]

print(f"DuckDB column count: {column_count}")


# Inspect first record
first_row = conn.execute("""
    SELECT *
    FROM raw.marketing_campaign
    LIMIT 1
""").fetchone()

print(f"First row: {first_row}")



# end: conn
conn.close()


