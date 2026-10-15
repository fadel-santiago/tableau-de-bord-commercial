-- SQLite: revenues represent completed orders after discounts (EUR).
-- 1) Monthly revenue and number of completed orders
SELECT month, ROUND(SUM(revenue_eur),2) AS revenue_eur,
       SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END) AS completed_orders
FROM sales GROUP BY month ORDER BY month;

-- 2) Performance by region
SELECT region, ROUND(SUM(revenue_eur),2) AS revenue_eur,
       COUNT(DISTINCT CASE WHEN status='Completed' THEN customer_id END) AS paying_customers
FROM sales GROUP BY region ORDER BY revenue_eur DESC;

-- 3) Top 5 products
SELECT product, ROUND(SUM(revenue_eur),2) AS revenue_eur
FROM sales GROUP BY product ORDER BY revenue_eur DESC LIMIT 5;

-- 4) Revenue contribution by channel
SELECT channel, ROUND(SUM(revenue_eur),2) AS revenue_eur
FROM sales GROUP BY channel ORDER BY revenue_eur DESC;

-- 5) Year-on-year annual revenue growth
WITH yearly AS (
 SELECT year, SUM(revenue_eur) AS revenue_eur FROM sales GROUP BY year
)
SELECT year, ROUND(revenue_eur,2) AS revenue_eur,
       ROUND(100.0 * (revenue_eur / NULLIF(LAG(revenue_eur) OVER (ORDER BY year),0)-1),2) AS yoy_growth_pct
FROM yearly ORDER BY year;
