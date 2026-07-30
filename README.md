# Banking Analytics Pipeline

A relational banking database modeling customers, accounts, transactions, cards, loans, and compliance data — built to practice real-world data engineering and analytical SQL patterns used in banking.

## Schema

15 tables covering the full lifecycle of banking data:

`branches`, `employees`, `customers`, `account_types`, `accounts`, `transaction_types`, `transactions`, `cards`, `card_transactions`, `loan_types`, `loans`, `loan_payments`, `kyc_records`, `aml_alerts`, `audit_log`

Full schema: [`sql/schema.sql`](sql/schema.sql)

## Data

Synthetic but realistic data generated with Python (Faker), loaded into the schema:

| Table | Rows |
|---|---|
| transactions | 5,000 |
| card_transactions | 1,500 |
| audit_log | 1,000 |
| loan_payments | 900 |
| accounts | 700 |
| customers / kyc_records | 500 each |
| cards | 400 |
| loans | 150 |
| employees | 50 |
| branches | 10 |
| **Total** | **10,788 rows** |

Generation script: [`scripts/generate_data.py`](scripts/generate_data.py)

## Analytical Queries

Queries demonstrating joins, CTEs, and window functions against the dataset — e.g., ranking accounts by deposits within each branch, running balances over time, and monthly transaction trend analysis.

Full queries: [`sql/analytical_queries.sql`](sql/analytical_queries.sql)
Sample output: [`sql/sample_query_output.txt`](sql/sample_query_output.txt)

## Query Performance

Benchmarked a common lookup pattern (fetching all transactions for a given account — 300 lookups across random accounts) before and after adding an index on the foreign key:

| | Time (300 lookups) |
|---|---|
| Without index | 56.0 ms |
| With index | 4.2 ms |

**Result: ~93% reduction in query time (13.5x speedup)** by indexing `transactions.account_id`.

## Tech Stack

MySQL Workbench (design) · SQLite (local testing/benchmarking) · Python (Faker for data generation)

## Notes

Data in this project is synthetic and generated for practice purposes — it does not represent any real institution's data.
