
  create view "airflow"."public"."my_first_model__dbt_tmp"
    
    
  as (
    -- Simple example model
SELECT 1 as id, 'Example' as name
UNION ALL
SELECT 2 as id, 'Test' as name
  );