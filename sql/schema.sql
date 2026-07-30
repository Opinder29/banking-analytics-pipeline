CREATE TABLE branches (
    branch_id INTEGER PRIMARY KEY,
    branch_name TEXT NOT NULL,
    city TEXT NOT NULL,
    province TEXT NOT NULL
);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    branch_id INTEGER NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL,
    hire_date DATE NOT NULL,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    signup_date DATE NOT NULL,
    branch_id INTEGER NOT NULL,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE account_types (
    account_type_id INTEGER PRIMARY KEY,
    type_name TEXT NOT NULL,
    interest_rate REAL NOT NULL
);

CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    account_type_id INTEGER NOT NULL,
    branch_id INTEGER NOT NULL,
    opened_date DATE NOT NULL,
    status TEXT NOT NULL,
    balance REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (account_type_id) REFERENCES account_types(account_type_id),
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE transaction_types (
    transaction_type_id INTEGER PRIMARY KEY,
    type_name TEXT NOT NULL
);

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    transaction_type_id INTEGER NOT NULL,
    transaction_date DATETIME NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_types(transaction_type_id)
);

CREATE TABLE cards (
    card_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    card_type TEXT NOT NULL,
    issue_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE card_transactions (
    card_transaction_id INTEGER PRIMARY KEY,
    card_id INTEGER NOT NULL,
    merchant TEXT NOT NULL,
    transaction_date DATETIME NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (card_id) REFERENCES cards(card_id)
);

CREATE TABLE loan_types (
    loan_type_id INTEGER PRIMARY KEY,
    type_name TEXT NOT NULL,
    base_rate REAL NOT NULL
);

CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    loan_type_id INTEGER NOT NULL,
    principal_amount REAL NOT NULL,
    start_date DATE NOT NULL,
    term_months INTEGER NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (loan_type_id) REFERENCES loan_types(loan_type_id)
);

CREATE TABLE loan_payments (
    payment_id INTEGER PRIMARY KEY,
    loan_id INTEGER NOT NULL,
    payment_date DATE NOT NULL,
    amount_paid REAL NOT NULL,
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id)
);

CREATE TABLE kyc_records (
    kyc_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    verification_status TEXT NOT NULL,
    verified_date DATE,
    id_type TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE aml_alerts (
    alert_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    transaction_id INTEGER,
    alert_reason TEXT NOT NULL,
    alert_date DATETIME NOT NULL,
    resolved INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);

CREATE TABLE audit_log (
    log_id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    table_affected TEXT NOT NULL,
    action_date DATETIME NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
