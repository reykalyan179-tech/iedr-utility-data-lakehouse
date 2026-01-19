# IEDR Utility Data Lakehouse – Architecture Overview

## Project Goal
Build a scalable, harmonized data platform to ingest, clean, and serve utility circuit/hosting capacity and DER (Distributed Energy Resource) data from multiple New York utilities.

Supports the IEDR SaaS application by providing:
- Feeders with max hosting capacity > X MW (single query)
- All installed and planned DERs for a given feeder ID (single query)

## Key Requirements (from interview task)
- Monthly incremental updates (additions + changes to existing records)
- Common data model across utilities (hide source differences)
- Handle utility differences:
  - Utility1: circuit segments → must aggregate to feeder level
  - Utility2: full feeders → direct use
- Use medallion architecture (bronze → silver → platinum)
- Data quality visibility (refresh dates, missing data, summaries)

## High-Level Architecture
- **Ingestion** → Raw CSVs uploaded to Databricks DBFS / Volumes
- **Bronze Layer** → Raw data as Delta tables (append or merge for updates)
- **Silver Layer** → Cleaned + normalized:
  - Common `feeder_id`
  - Hosting capacity in MW
  - Aggregated DER counts and details
  - Unified schema across utilities
- **Platinum Layer** → Query-optimized tables:
  - `feeder_capacity`: feeder_id, max_hosting_capacity_mw, installed_der_count, planned_der_count, ...
  - `der_details`: detailed installed/planned DER records per feeder
  - `data_quality_summary`: metadata (last refresh, row counts, missing values)

## Tech Stack (Free Tier Compatible)
- Databricks Community Edition (PySpark, Delta Lake, Notebooks, Jobs)
- GitHub (version control + basic CI via GitHub Actions)
- Simulated environments: folder-based (/iedr_dev, /iedr_qa, /iedr_prod)

## SDLC Approach
- Branches: main (prod), develop (integration), feature/*
- PR reviews + basic CI checks
- Manual promotion to QA/prod folders (due to free tier limits)

## Next Steps
- Setup Databricks Community Edition workspace
- Upload sample CSVs
- Build bronze ingestion pipeline
