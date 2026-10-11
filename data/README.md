# Data Directory

This directory contains the source datasets used by the Analytics Engineering platform.

## Structure

```text
data/
├── README.md
└── raw/
    ├── marketing_campaign_2024.csv
    ├── marketing_campaign_2025.csv
    └── marketing_campaign_jul_dec_2024.csv
```

## Data Pipeline

The raw CSV files serve as the input for the data pipeline:

1. **Ingestion:** Python loads the source files into the DuckDB raw layer.
2. **Transformation:** dbt transforms the ingested data through staging, intermediate, and mart models.
3. **Data Quality:** Tests validate data integrity and model correctness.
4. **Serving:** The resulting analytical models are made available through PostgreSQL.

The raw source files are preserved as inputs to the pipeline and are not used as transformation outputs.

