# Validate source CSV against DuckDB raw table

from pathlib import Path
import csv
import duckdb


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Source CSV
SOURCE_FILE = PROJECT_ROOT / "data" / "raw" / "marketing_campaign_2024.csv"

# DuckDB database
DATABASE_FILE = PROJECT_ROOT / "marketing_analytics.duckdb"


# --------------------------------------------------
# SOURCE VALIDATION
# --------------------------------------------------

with open(SOURCE_FILE, "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)

    source_columns = next(reader)
    source_records = list(reader)

source_row_count = len(source_records)
source_column_count = len(source_columns)


# --------------------------------------------------
# DUCKDB VALIDATION
# --------------------------------------------------

conn = duckdb.connect(DATABASE_FILE)

duckdb_row_count = conn.execute("""
    SELECT COUNT(*)
    FROM raw.marketing_campaign_2024
""").fetchone()[0]


duckdb_column_count = conn.execute("""
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = 'raw'
      AND table_name = 'marketing_campaign_2024'
""").fetchone()[0]

# for Reconciliation / Comparison, fetch all records from DuckDB
duckdb_records = conn.execute("""
    SELECT *
    FROM raw.marketing_campaign_2024
    ORDER BY campaign_id
""").fetchall()

# --------------------------------------------------
# COMPARE SOURCE VS DUCKDB
# --------------------------------------------------

row_count_match = source_row_count == duckdb_row_count
column_count_match = source_column_count == duckdb_column_count

# --------------------------------------------------
# DUCKDB SCHEMA / DATA TYPE VALIDATION
# --------------------------------------------------

schema_info = conn.execute("""
    SELECT
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema = 'raw'
      AND table_name = 'marketing_campaign_2024'
    ORDER BY ordinal_position
""").fetchall()


# --------------------------------------------------
# EXPECTED SCHEMA
# --------------------------------------------------

expected_schema = {
    "campaign_id": "VARCHAR",
    "campaign_name": "VARCHAR",
    "start_date": "DATE",
    "end_date": "DATE",
    "channel": "VARCHAR",
    "region": "VARCHAR",
    "impressions": "BIGINT",
    "clicks": "BIGINT",
    "conversions": "BIGINT",
    "spend_usd": "DOUBLE",
    "revenue_usd": "DOUBLE",
    "target_audience": "VARCHAR",
    "product_category": "VARCHAR",
    "device": "VARCHAR",
    "year": "BIGINT",
}

# --------------------------------------------------
# SCHEMA / DATA TYPE CHECK
# --------------------------------------------------

actual_schema = {
    column_name: data_type
    for column_name, data_type in schema_info
}

schema_match = actual_schema == expected_schema

# --------------------------------------------------
# OVERALL VALIDATION
# --------------------------------------------------

# overall_passed = row_count_match and column_count_match
overall_passed = (
    row_count_match
    and column_count_match
    and schema_match
)

# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("========================================")
print("MARKETING CAMPAIGN INGESTION VALIDATION")
print("========================================")

print("\nSOURCE")
print(f"Rows:    {source_row_count}")
print(f"Columns: {source_column_count}")

print("\nDUCKDB")
print(f"Rows:    {duckdb_row_count}")
print(f"Columns: {duckdb_column_count}")

print("\n----------------------------------------")

print(
    f"ROW COUNT CHECK       "
    f"{'PASSED' if row_count_match else 'FAILED'}"
)

print(
    f"COLUMN COUNT CHECK    "
    f"{'PASSED' if column_count_match else 'FAILED'}"
)

print(
    f"SCHEMA / DATA TYPE CHECK   "
    f"{'PASSED' if schema_match else 'FAILED'}"
)

print("----------------------------------------")

print(
    f"VALIDATION RESULT: "
    f"{'PASSED' if overall_passed else 'FAILED'}"
)

print("========================================")


# --------------------------------------------------
# SCHEMA DETAILS
# --------------------------------------------------

print("\n========================================")
print("SCHEMA / DATA TYPE VALIDATION")
print("========================================")

print(f"\nDUCKDB COLUMNS: {len(schema_info)}")

print("\nCOLUMN                 DUCKDB TYPE")
print("----------------------------------------")

for column_name, data_type in schema_info:
    print(f"{column_name:<22} {data_type}")



print(
    f"\nSCHEMA / DATA TYPE CHECK   "
    f"{'PASSED' if schema_match else 'FAILED'}"
)

# --------------------------------------------------
# NULL VALUE VALIDATION
# --------------------------------------------------

null_counts = conn.execute("""
    SELECT
        COUNT(*) - COUNT(campaign_id) AS campaign_id_nulls,
        COUNT(*) - COUNT(campaign_name) AS campaign_name_nulls,
        COUNT(*) - COUNT(start_date) AS start_date_nulls,
        COUNT(*) - COUNT(end_date) AS end_date_nulls,
        COUNT(*) - COUNT(channel) AS channel_nulls,
        COUNT(*) - COUNT(region) AS region_nulls,
        COUNT(*) - COUNT(impressions) AS impressions_nulls,
        COUNT(*) - COUNT(clicks) AS clicks_nulls,
        COUNT(*) - COUNT(conversions) AS conversions_nulls,
        COUNT(*) - COUNT(spend_usd) AS spend_usd_nulls,
        COUNT(*) - COUNT(revenue_usd) AS revenue_usd_nulls,
        COUNT(*) - COUNT(target_audience) AS target_audience_nulls,
        COUNT(*) - COUNT(product_category) AS product_category_nulls,
        COUNT(*) - COUNT(device) AS device_nulls,
        COUNT(*) - COUNT(year) AS year_nulls
    FROM raw.marketing_campaign_2024
""").fetchone()


print("\n========================================")
print("NULL VALUE VALIDATION")
print("========================================")

null_columns = [
    (column, count)
    for column, count in zip(expected_schema.keys(), null_counts)
    if count > 0
]

if null_columns:
    for column, count in null_columns:
        print(f"{column:<22} NULLS: {count}")
else:
    print("No NULL values found.")

# --------------------------------------------------
# DUPLICATE CAMPAIGN ID VALIDATION
# --------------------------------------------------

duplicate_campaigns = conn.execute("""
    SELECT
        campaign_id,
        COUNT(*) AS record_count
    FROM raw.marketing_campaign_2024
    GROUP BY campaign_id
    HAVING COUNT(*) > 1
    ORDER BY record_count DESC, campaign_id
""").fetchall()


print("\n========================================")
print("DUPLICATE CAMPAIGN ID VALIDATION")
print("========================================")

if duplicate_campaigns:
    for campaign_id, record_count in duplicate_campaigns:
        print(
            f"{campaign_id:<20} "
            f"RECORDS: {record_count}"
        )
else:
    print("No duplicate campaign IDs found.")


# --------------------------------------------------
# NUMERIC VALUE VALIDATION
# --------------------------------------------------

negative_values = conn.execute("""
    SELECT
        SUM(CASE WHEN impressions < 0 THEN 1 ELSE 0 END) AS negative_impressions,
        SUM(CASE WHEN clicks < 0 THEN 1 ELSE 0 END) AS negative_clicks,
        SUM(CASE WHEN conversions < 0 THEN 1 ELSE 0 END) AS negative_conversions,
        SUM(CASE WHEN spend_usd < 0 THEN 1 ELSE 0 END) AS negative_spend,
        SUM(CASE WHEN revenue_usd < 0 THEN 1 ELSE 0 END) AS negative_revenue
    FROM raw.marketing_campaign_2024
""").fetchone()


print("\n========================================")
print("NUMERIC VALUE VALIDATION")
print("========================================")

numeric_checks = {
    "impressions": negative_values[0],
    "clicks": negative_values[1],
    "conversions": negative_values[2],
    "spend_usd": negative_values[3],
    "revenue_usd": negative_values[4],
}

negative_columns = [
    (column, count)
    for column, count in numeric_checks.items()
    if count > 0
]

if negative_columns:
    for column, count in negative_columns:
        print(f"{column:<22} NEGATIVE VALUES: {count}")
else:
    print("No negative values found in campaign measures.")


# --------------------------------------------------
# DATE RELATIONSHIP VALIDATION
# --------------------------------------------------

invalid_date_ranges = conn.execute("""
    SELECT COUNT(*)
    FROM raw.marketing_campaign_2024
    WHERE start_date > end_date
""").fetchone()[0]


print("\n========================================")
print("DATE RELATIONSHIP VALIDATION")
print("========================================")

if invalid_date_ranges > 0:
    print(
        f"Invalid date ranges found: "
        f"{invalid_date_ranges}"
    )
else:
    print("No invalid date ranges found.")


# --------------------------------------------------
# CAMPAIGN LOGIC DETAIL
# --------------------------------------------------

logic_detail = conn.execute("""
    SELECT
        SUM(CASE WHEN clicks > impressions THEN 1 ELSE 0 END)
            AS clicks_exceed_impressions,

        SUM(CASE WHEN conversions > clicks THEN 1 ELSE 0 END)
            AS conversions_exceed_clicks,

        SUM(
            CASE
                WHEN clicks > impressions
                 AND conversions > clicks
                THEN 1
                ELSE 0
            END
        ) AS both_rules_violated,

        COUNT(*) AS total_records

    FROM raw.marketing_campaign_2024
""").fetchone()


print("\n========================================")
print("CAMPAIGN LOGIC DETAIL")
print("========================================")

print(
    f"Clicks > impressions: "
    f"{logic_detail[0]}"
)

print(
    f"Conversions > clicks: "
    f"{logic_detail[1]}"
)

print(
    f"Both rules violated: "
    f"{logic_detail[2]}"
)

print(
    f"Total records: "
    f"{logic_detail[3]}"
)

# --------------------------------------------------
# CAMPAIGN LOGIC EXAMPLES
# --------------------------------------------------

invalid_examples = conn.execute("""
    SELECT
        campaign_id,
        impressions,
        clicks,
        conversions
    FROM raw.marketing_campaign_2024
    WHERE clicks > impressions
       OR conversions > clicks
    LIMIT 10
""").fetchall()


print("\n========================================")
print("CAMPAIGN LOGIC EXAMPLES")
print("========================================")

print(
    "\nCAMPAIGN ID            IMPRESSIONS    CLICKS    CONVERSIONS"
)
print("------------------------------------------------------------")

for campaign_id, impressions, clicks, conversions in invalid_examples:
    print(
        f"{campaign_id:<22}"
        f"{impressions:<15}"
        f"{clicks:<10}"
        f"{conversions}"
    )


# --------------------------------------------------
# MEASURE ORDERING INVESTIGATION
# --------------------------------------------------

measure_ordering = conn.execute("""
    SELECT
        SUM(
            CASE
                WHEN impressions != clicks
                 AND impressions != conversions
                 AND clicks != conversions
                THEN 1
                ELSE 0
            END
        ) AS distinct_measure_values,

        SUM(
            CASE
                WHEN impressions = clicks
                  OR impressions = conversions
                  OR clicks = conversions
                THEN 1
                ELSE 0
            END
        ) AS tied_measure_values,

        COUNT(*) AS total_records

    FROM raw.marketing_campaign_2024
""").fetchone()


print("\n========================================")
print("MEASURE ORDERING INVESTIGATION")
print("========================================")

print(
    f"Records with three distinct values: "
    f"{measure_ordering[0]}"
)

print(
    f"Records with tied measure values: "
    f"{measure_ordering[1]}"
)

print(
    f"Total records: "
    f"{measure_ordering[2]}"
)

# --------------------------------------------------
# RECONSTRUCTION HYPOTHESIS TEST
# --------------------------------------------------

reconstruction_check = conn.execute("""
    SELECT
        COUNT(*)
    FROM raw.marketing_campaign_2024
    WHERE
        GREATEST(impressions, clicks, conversions)
        >
        (
            impressions
            + clicks
            + conversions
            - GREATEST(impressions, clicks, conversions)
            - LEAST(impressions, clicks, conversions)
        )
        AND
        (
            impressions
            + clicks
            + conversions
            - GREATEST(impressions, clicks, conversions)
            - LEAST(impressions, clicks, conversions)
        )
        >
        LEAST(impressions, clicks, conversions)
""").fetchone()[0]


print("\n========================================")
print("RECONSTRUCTION HYPOTHESIS TEST")
print("========================================")

print(
    f"Records with a valid "
    f"largest > middle > smallest ordering: "
    f"{reconstruction_check}"
)


# --------------------------------------------------
# CORRECTED MEASURE PREVIEW
# --------------------------------------------------

corrected_examples = conn.execute("""
    SELECT
        campaign_id,

        impressions AS raw_impressions,
        clicks AS raw_clicks,
        conversions AS raw_conversions,

        GREATEST(impressions, clicks, conversions)
            AS corrected_impressions,

        (
            impressions
            + clicks
            + conversions
            - GREATEST(impressions, clicks, conversions)
            - LEAST(impressions, clicks, conversions)
        ) AS corrected_clicks,

        LEAST(impressions, clicks, conversions)
            AS corrected_conversions

    FROM raw.marketing_campaign_2024

    ORDER BY campaign_id

    LIMIT 10
""").fetchall()


print("\n========================================")
print("CORRECTED MEASURE PREVIEW")
print("========================================")

print(
    "\nCAMPAIGN ID            "
    "RAW IMP    RAW CLICK  RAW CONV   "
    "CORR IMP   CORR CLICK  CORR CONV"
)

print(
    "--------------------------------------------------------------------------"
)

for (
    campaign_id,
    raw_impressions,
    raw_clicks,
    raw_conversions,
    corrected_impressions,
    corrected_clicks,
    corrected_conversions
) in corrected_examples:

    print(
        f"{campaign_id:<22}"
        f"{raw_impressions:<11}"
        f"{raw_clicks:<11}"
        f"{raw_conversions:<11}"
        f"{corrected_impressions:<11}"
        f"{corrected_clicks:<12}"
        f"{corrected_conversions}"
    )


# --------------------------------------------------
# CORRECTED FUNNEL VALIDATION
# --------------------------------------------------

corrected_funnel_check = conn.execute("""
    SELECT
        COUNT(*)
    FROM raw.marketing_campaign_2024
    WHERE
        (
            impressions
            + clicks
            + conversions
            - GREATEST(impressions, clicks, conversions)
            - LEAST(impressions, clicks, conversions)
        )
        >
        GREATEST(impressions, clicks, conversions)

        OR

        LEAST(impressions, clicks, conversions)
        >
        (
            impressions
            + clicks
            + conversions
            - GREATEST(impressions, clicks, conversions)
            - LEAST(impressions, clicks, conversions)
        )
""").fetchone()[0]


print("\n========================================")
print("CORRECTED FUNNEL VALIDATION")
print("========================================")

print(
    f"Corrected records violating "
    f"impressions > clicks > conversions: "
    f"{corrected_funnel_check}"
)


# Close DuckDB connection
conn.close()