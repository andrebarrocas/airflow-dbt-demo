
  
    

  create  table "airflow"."public"."fct_customer_purchase_patterns__dbt_tmp"
  
  
    as
  
  (
    

WITH customer_orders AS (
    SELECT
        customer_id,
        order_date,
        amount,
        LAG(order_date) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
        ) as previous_order_date
    FROM "airflow"."public"."stg_orders"
),

customer_metrics AS (
    SELECT
        customer_id,
        COUNT(*) as total_orders,
        SUM(amount) as total_amount,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date,
        AVG(amount) as avg_order_amount,
        -- Use PostgreSQL's date subtraction
        AVG(
            CASE 
                WHEN previous_order_date IS NOT NULL 
                THEN DATE_PART('day', order_date::timestamp - previous_order_date::timestamp)
            END
        ) as avg_days_between_orders
    FROM customer_orders
    GROUP BY customer_id
)

SELECT
    customer_id,
    total_orders,
    total_amount,
    first_order_date,
    last_order_date,
    avg_order_amount,
    avg_days_between_orders,
    CASE
        WHEN total_orders >= 10 THEN 'High'
        WHEN total_orders >= 5 THEN 'Medium'
        ELSE 'Low'
    END as frequency_segment,
    CASE
        WHEN avg_order_amount >= 200 THEN 'Premium'
        WHEN avg_order_amount >= 100 THEN 'Standard'
        ELSE 'Basic'
    END as value_segment
FROM customer_metrics
  );
  