SELECT 
    1 as order_id,
    'Product A' as product_name,
    100.00 as amount,
    CURRENT_DATE as order_date
UNION ALL
SELECT 
    2 as order_id,
    'Product B' as product_name,
    150.00 as amount,
    CURRENT_DATE as order_date 