-- Banking Analytics Pipeline — Analytical Queries
-- Demonstrates joins, CTEs, and window functions against real generated data

-- 1. Top 10 customers by total transaction volume (JOIN + aggregate)
SELECT c.customer_id, c.first_name, c.last_name, SUM(t.amount) AS total_volume
FROM customers c
JOIN accounts a ON a.customer_id = c.customer_id
JOIN transactions t ON t.account_id = a.account_id
GROUP BY c.customer_id
ORDER BY total_volume DESC
LIMIT 10;

-- 2. Running balance per account over time (WINDOW FUNCTION)
SELECT
    account_id,
    transaction_date,
    amount,
    SUM(amount) OVER (PARTITION BY account_id ORDER BY transaction_date) AS running_balance
FROM transactions
WHERE account_id = 1
ORDER BY transaction_date;

-- 3. Rank accounts by total deposits within each branch (CTE + WINDOW FUNCTION)
WITH branch_deposits AS (
    SELECT
        a.branch_id,
        a.account_id,
        SUM(t.amount) AS total_deposits
    FROM accounts a
    JOIN transactions t ON t.account_id = a.account_id
    WHERE t.amount > 0
    GROUP BY a.branch_id, a.account_id
)
SELECT
    branch_id,
    account_id,
    total_deposits,
    RANK() OVER (PARTITION BY branch_id ORDER BY total_deposits DESC) AS branch_rank
FROM branch_deposits
ORDER BY branch_id, branch_rank
LIMIT 20;

-- 4. Accounts with unusually large single transactions relative to their own history (CTE + window function)
WITH account_stats AS (
    SELECT
        account_id,
        AVG(amount) AS avg_amount,
        MAX(amount) AS max_amount
    FROM transactions
    GROUP BY account_id
)
SELECT
    account_id,
    avg_amount,
    max_amount,
    (max_amount - avg_amount) AS deviation
FROM account_stats
ORDER BY deviation DESC
LIMIT 10;

-- 5. Monthly transaction volume trend (date grouping + aggregate)
SELECT
    strftime('%Y-%m', transaction_date) AS month,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY month
ORDER BY month;
