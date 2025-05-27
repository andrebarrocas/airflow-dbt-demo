

-- Common interview question: implement a custom test
WITH validation AS (
    SELECT
        amount as value
    FROM "airflow"."public"."stg_orders"
    WHERE amount is not null
        
            AND amount < 0
        
)

SELECT *
FROM validation

