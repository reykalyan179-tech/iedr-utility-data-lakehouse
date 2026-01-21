IEDR Utility Data Lakehouse

This repository contains a Databricks-based data pipeline that ingests, cleans, and publishes utility data using a medallion architecture. The project demonstrates production-style data engineering practices including environment separation, CI/CD-driven deployments, and testable transformations.

What This Project Does

Ingests monthly utility CSV files

Preserves raw data with metadata for auditability

Normalizes and aggregates data into a unified model

Publishes API-ready tables for downstream applications

Deploys Databricks jobs using Git-based CI/CD

Supports separate dev, QA, and prod environments

Architecture

The pipeline follows a medallion pattern:

Bronze (Raw)

Raw CSV ingestion

No transformations

Metadata captured (source file, load timestamp)

Incremental loads supported

Silver (Transformed)

Column standardization

Data type normalization

Feeder-level aggregation

Basic data quality checks

Platinum (Serving)

Tables optimized for API access

Consolidated feeder and DER datasets

Data quality summary tables

Repository Structure
.
├── notebooks/
│   ├── bronze_ingest.ipynb
│   ├── silver_transformation.ipynb
│   └── platinum_publish.ipynb
├── tests/
│   └── test_transforms.py
├── ci/
│   └── deploy.yml
├── docs/
│   └── architecture.md
└── README.md

Environments

The same codebase is deployed to multiple environments:

dev – development and validation

qa – integration testing

prod – production runs

Environment-specific behavior is controlled through parameters passed at job runtime. No logic is duplicated between environments.

Deployment

Databricks jobs are deployed from Git using CI/CD.

Jobs are defined and managed as code

No manual UI changes are required

CI pipeline deploys jobs per environment

Git is the single source of truth

Testing

Transformation logic is covered by pytest unit tests

Tests validate business logic and expected outputs

CI runs tests on pull requests and merges

Notes

This project is intentionally scoped as a reference implementation.
The same patterns can be extended with orchestration, monitoring, and infrastructure-as-code for larger-scale production systems.
