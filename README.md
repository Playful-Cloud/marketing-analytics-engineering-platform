# Marketing Analytics Engineering Platform

An end-to-end marketing analytics project that combines data ingestion, warehouse modeling, SQL engineering, data quality, and business analysis to turn raw marketing campaign data into trusted analytical outputs.

---

## Project Overview

Marketing teams need reliable data to evaluate campaign performance, understand marketing efficiency, and make informed decisions about resource allocation.

This project builds a local Analytics Engineering platform that processes marketing campaign datasets through a structured data pipeline, applies tested SQL transformations, and supports downstream exploratory data analysis (EDA) and business analysis.

The project brings together **data engineering practices, analytics engineering, and business-focused analysis** in one integrated workflow.

---

## Objectives

- Build a reproducible ingestion workflow for raw marketing campaign data.
- Organize data transformations using a layered SQL and dbt modeling architecture.
- Establish data quality checks and validate business rules.
- Develop dimensional and fact models for analytical consumption.
- Support marketing performance analysis using SQL and Python.
- Document the architecture, transformation logic, quality controls, and business deliverables.

---

## Data Sources

The project uses three marketing campaign CSV files:

- `marketing_campaign_2024.csv`
- `marketing_campaign_2025.csv`
- `marketing_campaign_jul_dec_2024.csv`

Together, the source files contain **1,831 records across 15 columns** covering campaign attributes, engagement, conversions, spending, and revenue.

Key fields include campaign identifiers, campaign dates, marketing channels, regions, impressions, clicks, conversions, spend, revenue, target audiences, product categories, devices, and year.

**Explore the data:** [Data directory and raw source files](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/data)

---

### Data Directory Structure

```text
data/
├── README.md
└── raw/
    ├── marketing_campaign_2024.csv
    ├── marketing_campaign_2025.csv
    └── marketing_campaign_jul_dec_2024.csv
```

---

## Architecture & Workflow

```text
Raw Marketing Campaign CSVs
            |
            v
    Python Ingestion
    Inspection & Validation
            |
            v
       DuckDB Raw Layer
            |
            v
     dbt Transformations
            |
            v
    +---------------------+
    | Staging             |
    | Intermediate        |
    | Dimensions & Facts  |
    +---------------------+
            |
            v
    Data Quality Testing
    & Pipeline Validation
            |
            v
    PostgreSQL Serving
            |
            v
    SQL / Python EDA
    & Business Analysis
            |
            v
    Business Findings
    & Analytical Outputs
```

The workflow separates ingestion, transformation, quality assurance, serving, and analysis responsibilities.

- **Python** handles ingestion and initial data inspection and validation.
- **DuckDB** provides the local analytical warehouse and raw data layer.
- **dbt and SQL** implement modular transformations, model dependencies, and data quality tests.
- **PostgreSQL** serves the resulting analytical datasets.
- **SQL and Python** support downstream data exploration, analysis, and business interpretation.

---

### End-to-End Pipeline Responsibilities

| Stage | Responsibility | Implementation |
|---|---|---|
| Source | Store the original marketing campaign datasets. | CSV files |
| Ingestion | Load source data and perform initial inspection and validation. | Python |
| Raw warehouse | Store ingested source data. | DuckDB |
| Transformation | Prepare source data and apply reusable transformation logic. | SQL and dbt |
| Modeling | Publish campaign dimension and performance fact models. | dbt marts |
| Quality assurance | Validate model structure, relationships, measures, and selected business rules. | dbt tests and SQL |
| Serving | Make analytical datasets available downstream. | PostgreSQL |
| Analysis | Explore campaign performance and develop business findings. | SQL and Python |


---

## Analytics Engineering

The dbt project follows a layered modeling approach inspired by the Medallion Architecture, separating source preparation, reusable transformation logic, and analytical outputs.

| Layer | Responsibility |
|---|---|
| Staging | Expose and prepare source data for downstream transformations. |
| Intermediate | Apply reusable transformation logic and business rules. |
| Marts | Publish analytical dimension and fact models. |

The current analytical models include:

- **`dim_campaign`** — campaign identifiers and descriptive attributes.
- **`fct_campaign_performance`** — campaign-level performance measures, including impressions, clicks, conversions, spend, and revenue.

The fact model is designed at **one row per campaign**. This establishes a clear grain for downstream analysis and aggregation.

The modeling scope remains intentionally focused on current business requirements rather than introducing dimensions without a demonstrated analytical need.

---

### dbt Project Structure

```text
dbt_marketing_analytics_engineering/
├── models/
│   ├── staging/
│   │   └── stg_campaign_performance.sql
│   ├── intermediate/
│   │   ├── int_campaign_performance.sql
│   │   └── unit_tests.yml
│   ├── marts/
│   │   ├── dimensions/
│   │   │   └── dim_campaign.sql
│   │   └── facts/
│   │       └── fct_campaign_performance.sql
│   └── schema.yml
└── tests/
    └── Custom SQL data tests
```

*The tree highlights key models and test locations rather than listing every dbt configuration file or macro.*

**Explore the implementation:**

- [Complete dbt project](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering)
- [All dbt models](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/models)
- [Staging models](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/models/staging)
- [Intermediate models and unit tests](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/models/intermediate)
- [Mart models](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/models/marts)


---


## Data Quality & SQL Engineering

Quality assurance is integrated into the transformation workflow rather than treated as a final, separate step.

The project includes:

- **Generic dbt tests:** nullability, uniqueness, relationships, and accepted values.
- **Custom SQL data tests:** project-specific campaign measure and business-rule validations.
- **dbt unit tests:** controlled-input tests for selected transformation logic.
- **Reconciliation and pipeline validation:** checks designed to establish consistency across ingestion and transformation layers.
- **SQL engineering practices:** modular transformations, CTEs, joins, aggregations, conditional logic, derived metrics, and grain-aware modeling where applicable.

These controls help identify data issues, verify transformation assumptions, and improve confidence in the analytical outputs.

---

### Testing Resources

- [dbt data tests](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/tests) — custom SQL data tests and project-specific assertions.
- [Intermediate models and unit tests](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/models/intermediate) — transformation logic and associated unit-test definitions.

The different test types serve complementary purposes: data tests validate properties of the resulting data, while unit tests validate selected transformation behavior using controlled inputs and expected outputs.

---

## Business Analysis & Analytical Outputs

The platform extends beyond warehouse construction. Its modeled data supports downstream marketing EDA and business analysis.

The analytical work focuses on understanding campaign performance across engagement, conversion, spending, and revenue measures.

Relevant performance indicators include:

- Click-through rate (CTR)
- Conversion rate (CVR)
- Cost per click (CPC)
- Cost per acquisition (CPA)
- Cost per thousand impressions (CPM)
- Return on ad spend (ROAS)

These metrics must be calculated using appropriate numerator and denominator definitions and correctly aggregated measures, rather than blindly averaging campaign-level ratios.

The business analysis uses the data to investigate performance patterns and develop evidence-based findings and recommendations.

**Explore the analytical work:** [SQL Engineering & Business Analysis](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/analysis)

This work is part of the completed platform's scope, connecting technical data modeling to the business questions that the data is intended to answer.

---

## Technology Stack

| Area | Technology | Role |
|---|---|---|
| Ingestion and validation | Python | Load and inspect source datasets. |
| Data warehouse | DuckDB | Local analytical storage and raw data layer. |
| Transformation | SQL and dbt Core | Modular data modeling and ELT. |
| Data serving | PostgreSQL | Serve analytical datasets downstream. |
| Quality assurance | dbt tests and SQL | Validate data integrity and business rules. |
| Analysis | SQL and Python | Explore data and support business analysis. |
| Version control | Git and GitHub | Track project development and deliverables. |

---

## Repository Guide

The repository is organized by responsibility so reviewers can navigate directly to the implementation, technical documentation, and business deliverables.

---

### Root Directory

```text
marketing-analytics-engineering-platform/
├── analysis/                          # SQL engineering and business analysis
├── data/                              # Source datasets and data documentation
│   └── raw/                           # Raw marketing campaign CSV files
├── ingestion/                         # Python ingestion and validation
├── dbt_marketing_analytics_engineering/
│   ├── models/                        # SQL transformation models
│   └── tests/                         # dbt data tests
├── docs/                              # Architecture and project documentation
└── README.md                          # Project overview and navigation
```

This is a key-directory overview, not an exhaustive listing of every repository file.

---

### Implementation & Deliverables

| Resource | Purpose |
|---|---|
| [Data and raw files](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/data) | Source datasets and data documentation. |
| [Data ingestion and validation](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/ingestion) | Python ingestion components and related documentation. |
| [dbt project](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering) | Transformation project and configuration. |
| [All dbt models](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/models) | Staging, intermediate, and mart models. |
| [Staging models](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/models/staging) | Source preparation layer. |
| [Intermediate models](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/models/intermediate) | Reusable transformation logic and unit-test definitions. |
| [Mart models](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/models/marts) | Analytical dimensions and facts. |
| [dbt data tests](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/tests) | Custom SQL data tests and business-rule assertions. |
| [Project documentation](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/docs) | Architecture, design decisions, and technical documentation. |
| [SQL engineering and business analysis](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/analysis) | Downstream analytical work and business deliverables. |


---

## Documentation & Design Evidence

The project's documentation records the reasoning behind the architecture and modeling choices, not just the implementation itself.

The documentation directory is the main entry point for reviewing:

- Business problem definition and analytical requirements.
- Architecture and data flow.
- Warehouse design and modeling decisions.
- Data quality strategy and validation.
- Technical implementation and project decisions.

**[Browse Project Documentation](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/docs)**


---


## Running the Project

The intended workflow is to load the source datasets, build the dbt models, validate the results, and make the analytical data available for downstream use.

At a high level:

1. Review the source files in `data/raw/`.
2. Run the Python ingestion workflow in `ingestion/`.
3. Build and test the dbt project in `dbt_marketing_analytics_engineering/`.
4. Validate the resulting models and the PostgreSQL serving layer.
5. Explore the analytical outputs and business analysis in `analysis/`.

Exact setup commands depend on the project's current configuration, local database setup, and script entry points. Consult the relevant directory documentation before running the workflow. This README deliberately avoids prescribing unverified commands.

---

## Project Scope & Design Principles

This project emphasizes a practical, maintainable Analytics Engineering foundation:

- **Business-first modeling:** build models around demonstrated analytical requirements.
- **Explicit grain and keys:** define the level of detail represented by each model.
- **Layered transformations:** separate source preparation, reusable logic, and analytical outputs.
- **Testable data products:** validate structural integrity and selected business rules.
- **End-to-end thinking:** connect source ingestion, warehouse modeling, quality assurance, serving, and analysis.
- **Deliberate scope:** prioritize a complete, understandable local implementation before introducing additional infrastructure.

The current version focuses on a local SQL-based workflow using DuckDB, dbt, and PostgreSQL. Cloud deployment, orchestration, and containerization are not prerequisites for the core project.

---

## Outcome

The result is an integrated marketing analytics solution that demonstrates the work required to move from raw campaign datasets to structured, tested, and analysis-ready data—and then use that data to investigate business performance.

It showcases both the technical foundations of Analytics Engineering and the business context that gives the resulting data products their purpose.

---

