# dbt: nalytics Engineering

## Overview

This dbt project implements the transformation and analytical modeling layer of the Marketing Analytics Engineering Platform. It uses SQL-based transformations and modular data models to convert ingested raw campaign data into trusted, business-ready analytical datasets.

dbt separates transformation logic from ingestion, making the workflow easier to maintain, test, document, and extend as analytical requirements evolve.

## Modeling Approach

The project follows a layered modeling architecture inspired by the **Medallion Architecture**, organizing transformations into distinct stages:

- **Staging:** Standardizes and prepares source data for downstream processing.
- **Intermediate:** Applies reusable transformation logic and business rules.
- **Marts:** Publishes dimensional and fact models designed for analytical consumption.

This layered approach promotes separation of concerns, reusable SQL, clear dependencies, and maintainable data models.

## Data Quality & Testing

dbt tests are integrated into the modeling workflow to validate data integrity and model assumptions. These include checks for null values, uniqueness, relationships, accepted values, and selected business rules.

Testing helps identify data quality issues early and increases confidence in the analytical datasets produced by the pipeline.

## Transformation Workflow

```text
DuckDB Raw Layer
       ↓
    Staging
       ↓
  Intermediate
       ↓
      Marts
       ↓
 dbt Tests & Validation
       ↓
PostgreSQL Serving Layer
```

The workflow uses dbt's model references and dependency graph to organize transformations and support controlled execution.

## Objective

The goal is to establish a simple, modern Analytics Engineering workflow using SQL and dbt: modular transformations, explicit dependencies, tested data models, and trusted analytical outputs ready for downstream reporting and analysis.

## Models & Testing

### Models

The dbt models are organized into staging, intermediate, and marts layers to separate source preparation, reusable transformation logic, and analytical outputs.

- **[Browse dbt Models](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/models)**

### Testing Framework

Testing is integrated into the dbt workflow to validate data quality, transformation logic, and model reliability.

| Test Type | Purpose |
|---|---|
| **Generic Tests** | Reusable schema-level checks, such as `not_null`, `unique`, `relationships`, and `accepted_values`. These help enforce structural integrity and data quality expectations across models. |
| **Custom Tests** | Project-specific SQL assertions that validate business rules and data constraints not fully covered by generic tests. |
| **Unit Tests** | Validate model transformation logic against controlled input and expected output datasets before relying on the transformation in the full pipeline. |

**Implementation links:**

- **[Generic & Custom Tests](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/tests)** — reusable quality checks and project-specific SQL assertions.
- **[Intermediate Models & Unit Tests](https://github.com/Playful-Cloud/marketing-analytics-engineering-platform/tree/main/dbt_marketing_analytics_engineering/models/intermediate)** — intermediate transformation logic and associated unit-test definitions.

Together, these testing layers help catch structural issues, enforce business rules, and verify transformation behavior, increasing confidence in the analytical models produced by dbt.

