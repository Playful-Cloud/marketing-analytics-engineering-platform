\# Marketing Analytics Engineering Platform



An Analytics Engineering / Data Engineering project that transforms raw marketing campaign data into a reproducible, tested, and analytics-ready data platform.



\## Project Evolution



This project evolves from an initial Marketing Campaign Analysis project (V1) into a reusable Analytics Engineering platform (V2).



\### V1 — Marketing Campaign Analysis



The original project focused on analyzing campaign performance and answering business questions through analytical workflows.



\### V2 — Marketing Analytics Engineering Platform



The V2 project focuses on building the engineering foundation behind those analyses.



The platform emphasizes:



\- Data architecture

\- Data ingestion

\- Warehouse engineering

\- Dimensional modeling

\- SQL and dbt transformations

\- Data quality

\- Reproducibility

\- Documentation

\- Production readiness



\## Architecture



The planned platform follows this general flow:



```text

Raw CSV Sources

&#x20;     ↓

Python Ingestion

&#x20;     ↓

DuckDB Raw Layer

&#x20;     ↓

dbt + SQL

&#x20;     ↓

Staging

&#x20;     ↓

Intermediate

&#x20;     ↓

Marts

&#x20;     ↓

Business Data Products

&#x20;     ↓

PostgreSQL

&#x20;     ↓

Power BI / Python / ML

