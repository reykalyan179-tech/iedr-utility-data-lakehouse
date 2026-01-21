# IEDR Utility Data Lakehouse Pipeline

End-to-end data pipeline for the **Integrated Energy Data Resource (IEDR)** project, built to ingest, process, and serve utility data (circuits, installed DERs, planned DERs) from New York utilities in a cloud-based lakehouse.

This project was developed as part of a Data Engineer III interview task using **Databricks Premium Trial** (with $400 credits). It demonstrates a full **medallion architecture**, environment separation, Git integration, unit testing, CI, and job orchestration.

## Project Overview

The pipeline ingests raw CSV data from multiple utilities, normalizes it into a common model (handling differences like segment vs feeder level), and produces API-ready tables for the IEDR SaaS application.

### Key Requirements Satisfied

- Common data model across utilities (hides source differences)
- Supports two main API queries:
  - Feeders with max hosting capacity > X MW
  - All installed + planned DERs for a given feeder ID
- Highlights missing data, refresh dates, volume, and quality stats
- Monthly incremental updates (append mode in bronze)

## Medallion Architecture

- **Bronze Layer** — Raw ingestion of 6 CSVs (circuits, installed DER, planned DER) with metadata (utility_id, ingest_timestamp, source_file)
  - Tables: `utility1_circuits`, `utility1_install_der`, `utility1_planned_der`, etc.
  - Stored in `iedr_[env]_bronze` schemas

- **Silver Layer** — Normalization & unification
  - Aggregates utility1 segments to feeders
  - Combines installed/planned DERs with common columns (feeder_id, der_type, nameplate_rating_mw, status)
  - Tables: `feeders`, `der_records`
  - Stored in `iedr_[env]_silver`

- **Platinum Layer** — API-optimized
  - `feeder_capacity`: aggregated feeders with DER counts
  - `der_details`: detailed DER records per feeder
  - `data_quality_summary`: refresh dates, row counts, missing data
  - Stored in `iedr_[env]_platinum`

## Environments (Dev / QA / Prod)

Simulated using schema prefixes (`iedr_dev_*`, `iedr_qa_*`, `iedr_prod_*`) and jobs pass `env` parameter → same notebooks write to correct schemas.

## Git & Version Control

- Repo: https://github.com/reykalyan179-tech/iedr-utility-data-lakehouse
- Structure:
  - `notebooks/` — Databricks .ipynb files (bronze ingest, silver transform)
  - `tests/` — pytest unit tests
  - `my_project/` — DAB config (databricks.yml, resources/)
  - `docs/` — architecture documentation
  - `.github/workflows/` — CI pipeline

- Branching: main (production-ready), develop (integration), feature/* (new work)

## SDLC Process (DevOps Approach)

1. **Planning** — Define requirements, data model, env separation
2. **Development** — Build notebooks in Databricks, export to Git
3. **Testing** — Local pytest + GitHub Actions CI (lint + tests on push/PR)
4. **Deployment** — DAB deploy (`databricks bundle deploy -t dev/qa/prod`) → jobs updated
5. **Monitoring** — Job runs/logs in Workflows, data quality summary in platinum

Changes flow: Edit notebook → export → commit/push → CI runs → deploy → jobs run → data in correct env schemas.

GitHub Actions auto-deploys to separate dev/qa/prod workspaces.

## How the Pipeline Works

1. Raw CSVs uploaded to Volume (`iedr_raw`)
2. Bronze job loads CSVs to raw Delta tables in `iedr_[env]_bronze`
3. Silver job reads bronze → normalizes → saves to `iedr_[env]_silver`
4. Platinum logic (in silver notebook) creates API tables in `iedr_[env]_platinum`
5. Application queries platinum tables (e.g. `feeder_capacity WHERE max_hosting_capacity_mw > 5`)

## Setup & Run

1. Clone repo: git clone https://github.com/reykalyan179-tech/iedr-utility-data-lakehouse.git
2. Import notebooks to Databricks workspace.

3. Create Volume `iedr_raw` and upload 6 CSVs.

4. Run SQL to create schemas:
%sql
CREATE SCHEMA IF NOT EXISTS iedr_dev_bronze;
Repeat for silver/platinum, qa, prod

5. Deploy jobs with DAB:textcd my_project
databricks bundle deploy -t dev
databricks bundle deploy -t qa
databricks bundle deploy -t prod

6. Run jobs in Workflows

## Testing
pytest tests/ - GitHub Actions CI runs pytest + linting on every push/PR.


