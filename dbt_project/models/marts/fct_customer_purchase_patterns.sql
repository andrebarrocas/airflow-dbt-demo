{{
    config(
        materialized='table',
        tags=['daily']
    )
}}

WITH customer_purchases AS (
    SELECT
        customer_id,
        order_date,
        amount,
        -- Common interview question: calculate days between purchases
        LAG(order_date) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
        ) as previous_order_date,
        -- Calculate running total
        SUM(amount) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) as lifetime_spend
    FROM {{ ref('stg_orders') }}
    WHERE status = 'completed'
),

purchase_metrics AS (
    SELECT
        customer_id,
        order_date,
        amount,
        previous_order_date,
        lifetime_spend,
        -- Common interview question: handle NULL for first purchase
        COALESCE(
            DATE_DIFF('day', previous_order_date, order_date),
            0
        ) as days_since_previous_order
    FROM customer_purchases
)

SELECT
    customer_id,
    COUNT(*) as total_orders,
    AVG(amount) as avg_order_value,
    AVG(days_since_previous_order) as avg_days_between_orders,
    MAX(lifetime_spend) as total_lifetime_spend,
    -- Common interview question: categorize customers
    CASE 
        WHEN MAX(lifetime_spend) > 1000 THEN 'high_value'
        WHEN MAX(lifetime_spend) > 500 THEN 'medium_value'
        ELSE 'low_value'
    END as customer_segment
FROM purchase_metrics
GROUP BY 1 