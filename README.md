# M&A Financial Reconciliation & ETL Engine

## Overview
An automated financial data pipeline built in Python (Pandas) and SQLite designed to automate the ingestion, validation, and reconciliation of transactional datasets against general ledger (GL) balances. Developed to mirror enterprise banking reconciliation workflows.

## Key Features
- **Automated Data Ingestion:** Cleans and normalizes legacy transactional records and GL statements.
- **Accounting Validation:** Validates debit/credit entries and calculates net variances.
- **Audit Logging:** Flags discrepancies exceeding material thresholds ($0.01 CAD) for internal audit review.
- **Analytical Storage:** Exports reconciled datasets into an optimized SQLite database ready for BI consumption (Looker Studio / Power BI).

## Tech Stack
- Python (Pandas, NumPy)
- SQLite / SQL
- Logging & Error Handling
