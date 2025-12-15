-- ============================================
-- Project: Banking Credit Risk Analytics
-- File: 01_data_exploration.sql
-- Purpose: Explore credit card default behavior
-- ============================================

-- Preview the dataset
SELECT *
FROM credit_default
LIMIT 10;

-- Total number of customers
SELECT COUNT(*) AS total_customers
FROM credit_default;

-- Overall default rate
SELECT
    AVG(default_payment_next_month) AS default_rate
FROM credit_default;

-- Average credit limit by default status
SELECT
    default_payment_next_month,
    AVG(credit_limit) AS avg_credit_limit
FROM credit_default
GROUP BY default_payment_next_month;

-- Default rate by education level
SELECT
    education,
    AVG(default_payment_next_month) AS default_rate
FROM credit_default
GROUP BY education
ORDER BY default_rate DESC;

-- Default rate by age group
SELECT
    CASE
        WHEN age < 30 THEN 'Under 30'
        WHEN age BETWEEN 30 AND 50 THEN '30–50'
        ELSE 'Over 50'
    END AS age_group,
    AVG(default_payment_next_month) AS default_rate
FROM credit_default
GROUP BY age_group
ORDER BY default_rate DESC;
