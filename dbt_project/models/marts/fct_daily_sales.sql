{{
    config(
        materialized='table'
    )
}}

WITH daily_sales AS (
    SELECT
        DATE_TRUNC('day', order_date) as date,
        COUNT(DISTINCT order_id) as total_orders,
        COUNT(DISTINCT customer_id) as unique_customers,
        SUM(amount) as total_amount
    FROM {{ ref('stg_orders') }}
    WHERE status = 'completed'
    GROUP BY 1
)

SELECT
    date,
    total_orders,
    unique_customers,
    total_amount,
    total_amount / NULLIF(total_orders, 0) as avg_order_value,
    total_amount / NULLIF(unique_customers, 0) as avg_customer_spend
FROM daily_sales 