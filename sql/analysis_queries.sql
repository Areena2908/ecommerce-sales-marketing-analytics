-- E-commerce Sales & Marketing Analytics
-- SQL portfolio queries

-- 1. Monthly revenue and profit
SELECT
    strftime('%Y-%m', o.order_date) AS month,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
    ROUND(SUM(oi.quantity * (oi.unit_price - p.unit_cost)), 2) AS gross_profit,
    COUNT(DISTINCT o.order_id) AS orders
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY month
ORDER BY month;

-- 2. Product category performance
SELECT
    p.category,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
    ROUND(SUM(oi.quantity * (oi.unit_price - p.unit_cost)), 2) AS gross_profit,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    SUM(oi.quantity) AS units_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
GROUP BY p.category
ORDER BY revenue DESC;

-- 3. Channel revenue and ROAS
SELECT
    o.marketing_channel,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
    ROUND(SUM(ms.spend), 2) AS marketing_spend,
    ROUND(SUM(oi.quantity * oi.unit_price) / NULLIF(SUM(ms.spend), 0), 2) AS roas
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN marketing_spend ms
    ON strftime('%Y-%m', o.order_date) = ms.month
   AND o.marketing_channel = ms.channel
GROUP BY o.marketing_channel
ORDER BY roas DESC;

-- 4. Repeat customer behavior
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(total_amount) AS customer_revenue
    FROM orders
    GROUP BY customer_id
)
SELECT
    CASE WHEN order_count > 1 THEN 'Repeat' ELSE 'New/One-time' END AS customer_type,
    COUNT(*) AS customers,
    ROUND(AVG(order_count), 2) AS avg_orders,
    ROUND(AVG(customer_revenue), 2) AS avg_customer_revenue
FROM customer_orders
GROUP BY customer_type;

-- 5. Regional revenue
SELECT
    c.region,
    ROUND(SUM(o.total_amount), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(AVG(o.total_amount), 2) AS average_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.region
ORDER BY revenue DESC;

-- 6. Data quality checks
SELECT 'orders_missing_customer_id' AS check_name, COUNT(*) AS issue_count
FROM orders
WHERE customer_id IS NULL
UNION ALL
SELECT 'orders_negative_amount', COUNT(*)
FROM orders
WHERE total_amount < 0
UNION ALL
SELECT 'order_items_invalid_quantity', COUNT(*)
FROM order_items
WHERE quantity <= 0;
