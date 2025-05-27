select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      

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


      
    ) dbt_internal_test