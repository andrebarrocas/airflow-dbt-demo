
  create view "airflow"."public_staging"."stg_orders__dbt_tmp"
    
    
  as (
    

-- Staging model to clean and standardize raw orders data
SELECT
    order_id,
    customer_id,
    CAST(order_date AS DATE) as order_date,
    status,
    amount,
    CURRENT_TIMESTAMP as loaded_at
FROM "airflow"."raw"."orders"  -- This would point to your raw orders table
  );