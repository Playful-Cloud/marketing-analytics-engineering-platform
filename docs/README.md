# SQL Engineering & Data Quality

## Purpose

This document presents the engineering validation and evidence supporting the SQL and data-quality implementation of the marketing analytics engineering pipeline.

The objective was to establish that the analytical models are structurally sound, preserve the intended campaign grain, apply deterministic transformation logic, calculate derived metrics correctly, enforce appropriate data-quality rules, and maintain consistency across transformation layers.

---

## Scope

The engineering and validation work covered:

- baseline data and structural validation
- model grain and key validation
- SQL transformation hardening
- derived metrics and business logic
- dbt data-quality tests
- business-rule validation
- cross-layer reconciliation
- final pipeline execution
- SQL engineering evidence and implementation review

The scope focused on the existing marketing analytics pipeline from the validated raw DuckDB layer through the dbt transformation layers and analytical metrics model.

The work also evaluated whether additional SQL complexity or dimensional modeling was necessary. Patterns such as window functions, ranking, deduplication, complex joins, additional date transformations, and additional dimensions were not introduced where the current source grain and business requirements did not require them.

---

## Engineering Objectives

The engineering objectives were to:

- validate structural integrity across the analytical pipeline
- preserve the defined one-row-per-campaign grain
- validate primary-key completeness and uniqueness
- harden SQL transformation logic
- validate derived analytical metrics
- protect metric calculations against invalid denominators
- enforce appropriate dbt data-quality tests
- validate business rules supported by the dataset
- reconcile records and measures across transformation layers
- demonstrate practical SQL engineering patterns without introducing unnecessary complexity

---

## Data & Model Context

The pipeline operates on marketing campaign data ingested into DuckDB and transformed through dbt.

The central analytical grain is one row per campaign, identified by `campaign_id`.

The current dbt transformation structure consists of:

```text
Raw DuckDB
    ↓
stg_campaign_performance
    ↓
int_campaign_performance
    ├── dim_campaign
    └── fct_campaign_performance
            ↓
      campaign_metrics
```

The fact model contains campaign-level measures including:

- impressions
- clicks
- conversions
- spend_usd
- revenue_usd

The campaign dimension contains campaign descriptive attributes including:

- campaign name
- dates
- channel
- region
- target audience
- product category
- device
- year

Derived analytical metrics are calculated at campaign grain and include:

- CTR
- CPA
- CPC
- CPM
- ROI
- ROAS

---

## Validation & Engineering Areas

The engineering validation covered the major areas required to establish structural integrity, transformation correctness, analytical validity, and data-quality reliability across the current pipeline.

The validation areas were:

- baseline data and structural validation
- grain and key validation
- SQL transformation hardening
- derived metrics and business logic
- data-quality and business-rule validation
- cross-layer reconciliation
- final pipeline execution

Each area was evaluated against the defined campaign grain, business requirements, warehouse design, and implemented dbt models.

---

### Baseline Audit & Data Validation

The baseline validation established the structural condition of the dataset before evaluating downstream engineering behavior.

The validation covered:

- row counts
- expected columns
- data types
- NULL values
- duplicate campaign IDs
- numeric integrity
- date integrity
- categorical domains
- campaign funnel relationships
- transformation-layer consistency

The dataset contained 1,831 campaign records and maintained the expected 15-column source structure.

No NULL values or duplicate `campaign_id` values were identified in the validated layers.

Numeric measures were non-negative and populated across the validated dataset.

The campaign funnel investigation identified inconsistent ordering in the source measures. This supported the need for the dataset-specific measure reconstruction implemented in the intermediate model.

---

### Grain & Key Validation

The defined analytical grain is one row per campaign.

`campaign_id` was validated as the key across the relevant transformation layers.

The validation confirmed:

- 1,831 rows across the validated layers
- 1,831 distinct campaign IDs
- no duplicate campaign IDs
- no NULL campaign IDs
- no missing or extra campaign IDs between adjacent layers
- no fact-to-dimension fan-out
- one-to-one fact/dimension join behavior
- no grain conflicts in the dimension or fact models

The resulting model structure remains aligned with the warehouse design.

---

### SQL Transformation Hardening

The SQL transformation review evaluated whether the implemented models were deterministic, maintainable, and appropriate for the source data.

The intermediate model uses CTEs and a deterministic measure-reconstruction rule:

- largest source value → impressions
- middle source value → clicks
- smallest source value → conversions

The implementation was validated across all 1,831 campaigns.

The validation proved that the SQL implementation correctly and consistently applies the intended reconstruction rule.

It does not independently prove that the original source columns were semantically mislabeled.

Additional SQL patterns such as window functions, ranking, deduplication, complex joins, and unnecessary date transformations were evaluated but not introduced because they were not required by the current grain or business requirements.

---

### Derived Metrics & Business Logic

The analytical metrics layer provides campaign-level performance measures derived from the validated fact model.

The implementation was evaluated for metric definitions, calculation grain, aggregation behavior, denominator protection, placement, independent validation, and business relevance.

#### Metric Inventory

The analytical metric set consists of:

- CTR
- CPA
- CPC
- CPM
- ROI
- ROAS

Each metric is defined according to its business meaning and implemented at campaign grain.

#### Metric Grain

Derived metrics are calculated at the campaign level.

This preserves the one-row-per-campaign model while allowing the resulting measures to remain aggregation-safe for reporting and independent analytical validation.

#### Aggregation Strategy

The metric implementation calculates ratios at campaign grain.

Independent aggregate validation uses appropriate numerator and denominator aggregation, such as:

```sql
SUM(clicks) / SUM(impressions)

```
This aggregate calculation is used for validation and reporting behavior; it does not replace the row-level metric implementation.

---

#### Implemented Metrics

The analytical metrics implemented are:

| Metric | Formula |
|---|---|
| CTR | clicks / impressions |
| CPA | spend / conversions |
| CPC | spend / clicks |
| CPM | spend / impressions × 1,000 |
| ROI | (revenue − spend) / spend |
| ROAS | revenue / spend |

#### Metric Results

The validated aggregate results are:

| Metric | Validated result |
|---|---:|
| CTR | 33.42% |
| CPA | 1.99 |
| CPC | 0.90 |
| CPM | 300.80 |
| ROI | 168.95% |
| ROAS | 2.69x |

---

#### Zero/NULL Handling

Metric calculations use denominator guards to prevent invalid division.

The implementation follows the pattern:

```sql
CASE
    WHEN denominator > 0
    THEN numerator * 1.0 / denominator
    ELSE NULL
END

```
A controlled zero-denominator simulation confirmed that the six derived metrics return `NULL` rather than invalid results when their respective denominator is zero.

#### Metric Placement

Derived metrics are implemented in the analytical metrics layer rather than being stored as raw fact measures.

The fact model retains the underlying campaign-level measures, while `campaign_metrics` derives the analytical ratios from those measures.

#### Metric Validation

Independent benchmark calculations were compared against the model outputs.

The six metrics reconciled with the independent calculations.

Additional campaign-level spot checks confirmed that the formulas produce the expected results.

#### Business Interpretation

The metrics provide the required campaign-level performance indicators for:

- engagement
- acquisition efficiency
- cost efficiency
- media cost
- profitability
- advertising return

The metric set therefore remains aligned with the analytical requirements without introducing unnecessary metric complexity.

#### SQL Engineering Evidence

The implementation demonstrates practical SQL engineering patterns including:

- CTE-based transformation structure
- `CASE` expressions
- ratio calculations
- denominator protection
- aggregate validation
- deterministic transformations
- `ref()` and `source()` dependency management
- business-rule calculations
- grain-preserving transformations

Patterns such as window functions, ranking, deduplication, complex joins, and unnecessary date transformations were evaluated but were not required for the current implementation.

#### Assessment

The derived metrics and business logic were validated successfully.

No additional remediation was required.

---

### Data Quality & Business Rules

The data-quality strategy combines structural dbt tests with targeted business-rule validation.

The implementation includes:

- `not_null`
- `unique`
- `relationships`
- `accepted_values`
- custom business-rule tests

The business rules validate conditions supported by the current dataset and model design, including non-negative campaign measures and expected campaign-measure relationships.

The tests are intentionally targeted rather than exhaustive. Each test exists to enforce a specific structural, relational, categorical, or business requirement.

### Cross-Layer Reconciliation

Cross-layer validation confirmed record and key continuity across the transformation pipeline.

Validated layer relationships include:

```text
RAW
 ↓
STAGING
 ↓
INTERMEDIATE
 ↓
DIMENSION
 ↓
FACT

```

The reconciliation confirmed:

- consistent row populations
- consistent campaign keys
- no missing campaign IDs
- no extra campaign IDs
- no fact-to-dimension fan-out
- exact intermediate-to-fact measure reconciliation

This provides evidence that the transformation layers preserve the intended analytical population.

### Final Assessment

The final dbt execution completed successfully:

```text
4 models
26 data tests
1 unit test

PASS=31
WARN=0
ERROR=0
SKIP=0
NO-OP=0
REUSED=0
TOTAL=31

```

---

## Key Engineering Decisions

### Dataset-Specific Measure Reconstruction

The source dataset does not consistently preserve the expected semantic ordering of impressions, clicks, and conversions.

The intermediate transformation therefore reconstructs these measures by assigning the largest, middle, and smallest source values to impressions, clicks, and conversions respectively.

This is a dataset-specific reconstruction rule and should be revisited when a source with explicit semantic validation or reliable source metadata becomes available.

### Minimal Dimensional Model

The current warehouse design uses the smallest useful dimensional structure required by the current business requirements and source grain.

Additional dimensions were evaluated but not introduced where they would not provide independent analytical value.

### Targeted Data Quality

Data-quality tests were selected according to model grain, key requirements, relationships, categorical domains, measures, and supported business rules rather than applying blanket testing.

### No Artificial SQL Complexity

SQL patterns were evaluated according to whether they solved a current engineering or business requirement.

Window functions, ranking, deduplication, complex joins, additional date transformations, and additional dimensions were not introduced solely to demonstrate syntax.

## SQL Engineering Evidence

The implementation demonstrates evidence of:

- CTE-based transformations
- source and model dependencies
- deterministic business logic
- `CASE` expressions
- ratio calculations
- denominator protection
- aggregation-based validation
- grain preservation
- key validation
- business-rule testing
- cross-layer reconciliation

The complete validation queries and execution evidence are preserved in the accompanying evidence notebook.

---

## Data Quality Strategy

The data-quality implementation follows a layered approach:

```text
Structural validation
        ↓
Grain and key validation
        ↓
Transformation validation
        ↓
Metric validation
        ↓
Business-rule validation
        ↓
Cross-layer reconciliation
        ↓
Full dbt execution

```
The final automated dbt result was:

```text
PASS=31
WARN=0
ERROR=0
SKIP=0
NO-OP=0
REUSED=0
TOTAL=31

```
This provides executable evidence that the implemented models and tests complete successfully under the current dataset and project configuration.

---

## Scope Boundaries

The current implementation is a local batch analytical-engineering solution.

The following capabilities are outside the validated implementation:

- cloud infrastructure
- Databricks
- Spark
- Docker-based deployment
- production orchestration
- infrastructure as code
- production observability
- source-system freshness metadata
- advanced dimensional expansion beyond current requirements
- production-scale serving architecture
- production BI deployment

The absence of these capabilities is an intentional scope boundary rather than an implementation defect.

## Evidence

The supporting engineering evidence is preserved in:

`docs/SQL_Engineering_and_Data_Quality_evidence.ipynb`

The notebook contains the important validation SQL, execution results, independent metric checks, controlled simulations, reconciliation queries, and engineering interpretations supporting the claims in this document.

---


