"""
Generates realistic synthetic data for the Banking Analytics Pipeline
and loads it into a local SQLite DB (banking.db) for testing/validation.
Row counts are intentionally scaled to ~5,000 core transaction records,
with proportionate supporting data across the other 14 tables.
"""
import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

conn = sqlite3.connect("data/banking.db")
cur = conn.cursor()

with open("sql/schema.sql") as f:
    cur.executescript(f.read())

def rand_date(start_year=2020, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

# 1. branches
BRANCH_COUNT = 10
for i in range(1, BRANCH_COUNT + 1):
    cur.execute("INSERT INTO branches VALUES (?,?,?,?)",
                (i, f"{fake.city()} Branch", fake.city(), random.choice(["ON","BC","AB","QC","MB"])))

# 2. employees
EMPLOYEE_COUNT = 50
for i in range(1, EMPLOYEE_COUNT + 1):
    cur.execute("INSERT INTO employees VALUES (?,?,?,?,?,?)",
                (i, random.randint(1, BRANCH_COUNT), fake.first_name(), fake.last_name(),
                 random.choice(["Teller","Branch Manager","Loan Officer","Compliance Officer"]),
                 rand_date(2015, 2024).date().isoformat()))

# 3. customers
CUSTOMER_COUNT = 500
for i in range(1, CUSTOMER_COUNT + 1):
    cur.execute("INSERT INTO customers VALUES (?,?,?,?,?,?,?)",
                (i, fake.first_name(), fake.last_name(), fake.email(),
                 fake.date_of_birth(minimum_age=18, maximum_age=85).isoformat(),
                 rand_date(2018, 2025).date().isoformat(), random.randint(1, BRANCH_COUNT)))

# 4. account_types
account_types = [("Chequing", 0.001), ("Savings", 0.015), ("TFSA", 0.02), ("High-Interest Savings", 0.035), ("Business", 0.005)]
for i, (name, rate) in enumerate(account_types, start=1):
    cur.execute("INSERT INTO account_types VALUES (?,?,?)", (i, name, rate))

# 5. accounts
ACCOUNT_COUNT = 700
account_customer_map = []
for i in range(1, ACCOUNT_COUNT + 1):
    cust_id = random.randint(1, CUSTOMER_COUNT)
    account_customer_map.append(cust_id)
    cur.execute("INSERT INTO accounts VALUES (?,?,?,?,?,?,?)",
                (i, cust_id, random.randint(1, len(account_types)), random.randint(1, BRANCH_COUNT),
                 rand_date(2018, 2025).date().isoformat(), random.choice(["Active","Active","Active","Closed"]),
                 round(random.uniform(0, 50000), 2)))

# 6. transaction_types
txn_types = ["Deposit", "Withdrawal", "Transfer In", "Transfer Out", "Fee", "Interest Payment", "Cheque Deposit", "E-Transfer"]
for i, name in enumerate(txn_types, start=1):
    cur.execute("INSERT INTO transaction_types VALUES (?,?)", (i, name))

# 7. transactions (~5,000 — core table)
TRANSACTION_COUNT = 5000
for i in range(1, TRANSACTION_COUNT + 1):
    cur.execute("INSERT INTO transactions VALUES (?,?,?,?,?)",
                (i, random.randint(1, ACCOUNT_COUNT), random.randint(1, len(txn_types)),
                 rand_date(2023, 2025).isoformat(sep=" "), round(random.uniform(-2000, 5000), 2)))

# 8. cards
CARD_COUNT = 400
for i in range(1, CARD_COUNT + 1):
    issue = rand_date(2021, 2024).date()
    expiry = issue + timedelta(days=365 * 3)
    cur.execute("INSERT INTO cards VALUES (?,?,?,?,?,?)",
                (i, random.randint(1, ACCOUNT_COUNT), random.choice(["Debit","Credit"]),
                 issue.isoformat(), expiry.isoformat(),
                 random.choice(["Active","Active","Blocked","Expired"])))

# 9. card_transactions
CARD_TXN_COUNT = 1500
for i in range(1, CARD_TXN_COUNT + 1):
    cur.execute("INSERT INTO card_transactions VALUES (?,?,?,?,?)",
                (i, random.randint(1, CARD_COUNT), fake.company(),
                 rand_date(2023, 2025).isoformat(sep=" "), round(random.uniform(2, 400), 2)))

# 10. loan_types
loan_types = [("Personal Loan", 0.08), ("Mortgage", 0.045), ("Auto Loan", 0.065), ("Student Loan", 0.04), ("Business Loan", 0.07)]
for i, (name, rate) in enumerate(loan_types, start=1):
    cur.execute("INSERT INTO loan_types VALUES (?,?,?)", (i, name, rate))

# 11. loans
LOAN_COUNT = 150
for i in range(1, LOAN_COUNT + 1):
    cur.execute("INSERT INTO loans VALUES (?,?,?,?,?,?,?)",
                (i, random.randint(1, CUSTOMER_COUNT), random.randint(1, len(loan_types)),
                 round(random.uniform(2000, 400000), 2), rand_date(2019, 2024).date().isoformat(),
                 random.choice([12, 24, 36, 60, 120, 240]), random.choice(["Active","Active","Paid Off","Defaulted"])))

# 12. loan_payments
LOAN_PAYMENT_COUNT = 900
for i in range(1, LOAN_PAYMENT_COUNT + 1):
    cur.execute("INSERT INTO loan_payments VALUES (?,?,?,?)",
                (i, random.randint(1, LOAN_COUNT), rand_date(2023, 2025).date().isoformat(),
                 round(random.uniform(100, 3000), 2)))

# 13. kyc_records (one per customer)
for i in range(1, CUSTOMER_COUNT + 1):
    cur.execute("INSERT INTO kyc_records VALUES (?,?,?,?,?)",
                (i, i, random.choice(["Verified","Verified","Verified","Pending","Rejected"]),
                 rand_date(2018, 2025).date().isoformat(), random.choice(["Passport","Driver's License","PR Card"])))

# 14. aml_alerts
AML_ALERT_COUNT = 60
for i in range(1, AML_ALERT_COUNT + 1):
    cur.execute("INSERT INTO aml_alerts VALUES (?,?,?,?,?,?)",
                (i, random.randint(1, ACCOUNT_COUNT), random.randint(1, TRANSACTION_COUNT),
                 random.choice(["Large cash deposit","Rapid fund movement","Structuring pattern","High-risk jurisdiction transfer"]),
                 rand_date(2023, 2025).isoformat(sep=" "), random.choice([0, 1])))

# 15. audit_log
AUDIT_LOG_COUNT = 1000
for i in range(1, AUDIT_LOG_COUNT + 1):
    cur.execute("INSERT INTO audit_log VALUES (?,?,?,?,?)",
                (i, random.randint(1, EMPLOYEE_COUNT), random.choice(["INSERT","UPDATE","DELETE","VIEW"]),
                 random.choice(["accounts","transactions","customers","loans"]),
                 rand_date(2023, 2025).isoformat(sep=" ")))

conn.commit()

# Print row counts for verification
tables = ["branches","employees","customers","account_types","accounts","transaction_types",
          "transactions","cards","card_transactions","loan_types","loans","loan_payments",
          "kyc_records","aml_alerts","audit_log"]
print(f"{'Table':<20}{'Rows':>10}")
print("-" * 30)
total = 0
for t in tables:
    n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    total += n
    print(f"{t:<20}{n:>10}")
print("-" * 30)
print(f"{'TOTAL':<20}{total:>10}")

conn.close()
