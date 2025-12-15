-- ============================================
-- Project: Analytics Portfolio Project
-- File: 01_data_exploration.sql
-- Purpose: Initial data exploration and summary
-- ============================================

-- Preview the dataset
SELECT *
FROM dataset
LIMIT 10;

-- Count total records
SELECT COUNT(*) AS total_rows
FROM dataset;

-- Check for missing values in key fields
SELECT
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS missing_customer_id,
    SUM(CASE WHEN revenue IS NULL THEN 1 ELSE 0 END) AS missing_revenue
FROM dataset;

-- Basic summary statistics
SELECT
    AVG(revenue) AS avg_revenue,
    MIN(revenue) AS min_revenue,
    MAX(revenue) AS max_revenue
FROM dataset;

-- Grouped analysis example
SELECT
    region,
    COUNT(*) AS customers,
    AVG(revenue) AS avg_revenue
FROM dataset
GROUP BY region
ORDER BY avg_revenue DESC;
