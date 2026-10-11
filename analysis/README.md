# SQL Engineering & Business Analysis

## Overview

This project applies SQL engineering and business analysis to the Marketing Analytics Engineering Platform (V2), using structured marketing campaign data to evaluate campaign performance, marketing efficiency, and return on advertising spend (ROAS).

The work combines analytical SQL, data aggregation, derived performance metrics, and campaign-level comparisons to produce evidence-based findings and recommendations. It also documents the analytical data environment, execution workflow, and limitations to support reproducibility and reliable interpretation.

---

## Purpose & Scope

The purpose of this phase is to strengthen SQL engineering practices and translate modeled marketing data into actionable business insights.

**Scope includes:**
- Developing and validating SQL transformations, analytical queries, and derived performance metrics.
- Applying data quality checks and reconciling results across the analytical workflow.
- Evaluating campaign and channel performance, marketing efficiency, and campaign characteristics.
- Documenting business findings, recommendations, assumptions, and analytical limitations.

The analysis uses the project's modeled campaign data and focuses on descriptive performance assessment rather than causal attribution or predictive modeling.

---

## Objectives

### SQL Engineering
- Develop reliable, reusable SQL transformations and analytical queries.
- Validate model grain, keys, relationships, measures, and business rules.
- Support consistent and reproducible analytical outputs.

### Business Analysis
- Compare marketing performance and efficiency across channels.
- Identify high-performing campaigns and investigate low-ROAS results.
- Evaluate performance by region, product category, device, and target audience.
- Translate findings into evidence-based recommendations while documenting limitations.

---

## Technical Environment & Data Architecture

The analysis builds on the V2 analytics engineering workflow, using modeled marketing campaign data for SQL-based investigation and business reporting.

**Core technologies**
- **SQL** — transformations, aggregations, derived metrics, and business analysis.
- **Python** — data ingestion, inspection, validation, and pipeline execution.
- **DuckDB** — local analytical database used to execute the notebook queries.
- **dbt** — SQL model development, dependency management, and data quality testing.
- **PostgreSQL** — intended serving layer for downstream analytical consumption.

**Data flow**

Raw CSV files → Python ingestion → DuckDB raw layer → dbt transformations and analytical models → SQL business analysis.

The notebook executes against DuckDB views. PostgreSQL is documented separately as part of the serving workflow; its presence in the broader architecture does not imply that the notebook queries execute against PostgreSQL.

---

## Data Sources & Analytical Models

The analysis uses three CSV datasets containing marketing campaign records:

- `marketing_campaign_2024.csv`
- `marketing_campaign_2025.csv`
- `marketing_campaign_jul_dec_2024.csv`

Together, the datasets contain **1,831 records across 15 columns**, covering campaign attributes, dates, channels, regions, engagement, conversions, spend, and revenue.

The analysis uses the following dbt models:

| Model | Purpose |
|---|---|
| `dim_campaign` | Stores campaign attributes for filtering and comparison. |
| `fct_campaign_performance` | Stores campaign-level performance measures at one row per campaign. |
| `campaign_metrics` | Provides derived performance metrics used in the analysis. |

The models support comparisons across marketing channels, campaigns, regions, product categories, devices, and target audiences.

---

## SQL Engineering & Data Quality

The SQL engineering work emphasizes reliable analytical transformations, consistent metric calculations, and validation of modeled data.

Key practices include:
- Using SQL aggregations, joins, conditional logic, and derived metrics to support business questions.
- Preserving the campaign-level grain and validating campaign keys and model relationships.
- Applying dbt data tests to check required values, uniqueness, relationships, accepted categories, and business rules.
- Reconciling data across the ingestion and transformation layers and validating pipeline outputs.

Detailed test results and reconciliation evidence are maintained in the project's phase documentation.

---

## Business Analysis & Key Findings

The SQL analysis evaluates overall marketing performance, channel efficiency, campaign results, and performance differences across campaign characteristics.

The analysis covers:
- **Overall performance:** impressions, clicks, conversions, spend, revenue, CTR, and ROAS.
- **Channel efficiency:** CTR, cost per conversion, CPC, CPM, ROI ratio, and ROAS.
- **Campaign investigation:** top campaigns by revenue and ROAS, plus low-ROAS campaigns requiring further review.
- **Campaign characteristics:** performance comparisons by region, product category, device, and target audience.

### Key Findings

- Across 1,831 campaigns, aggregate ROAS was **2.69x**, based on total attributed revenue divided by total spend.
- Search and Social recorded the highest channel-level ROAS at **2.75x** each, while Display had the lowest at **2.61x**.
- Social had the lowest CPC at **$0.84**, while Display had the highest at **$1.06**.
- Services recorded the highest product-category ROAS at **3.33x**, while Automotive had the lowest at **2.36x**.
- The low-ROAS investigation identified campaigns for further review; these results support investigation rather than automatic campaign cancellation.

These findings are descriptive and depend on the validity of the underlying campaign measures and metric definitions.

---

## Limitations & Reproducibility

### Limitations
- The analysis is descriptive and does not establish causal relationships between campaign characteristics and performance.
- The source measures were reconstructed by ordering the original numeric values. Although the transformation is tested, the resulting measure assignments still require independent validation against their original business definitions.
- ROAS and other derived metrics depend on the correctness of the underlying spend, revenue, and campaign measures.
- Results are based on the available datasets and should not be treated as proof of overall campaign profitability.

### Reproducibility
- The SQL analysis notebook executes queries against the local DuckDB database and its analytical views.
- Python, DuckDB, and the required project models must be available in the local environment.
- Run the notebook from top to bottom to regenerate the analytical outputs.
- The original SQL reference file uses PostgreSQL-style schema references, while notebook execution uses DuckDB objects. Follow the notebook's documented environment setup when reproducing results.