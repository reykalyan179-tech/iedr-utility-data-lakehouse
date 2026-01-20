# IEDR Utility Data Lakehouse Pipeline

Cloud-based medallion architecture for NY utilities DER & hosting capacity data.

## Features
- Bronze: Raw ingestion from 6 CSVs
- Silver: Normalized feeders + unified DER records
- Platinum: API-ready tables (feeder_capacity, der_details)
- Env-aware: dev/qa/prod via parameter
- GitHub integration + Databricks Jobs
