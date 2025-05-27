

SELECT
    id::integer as user_id,
    name as full_name,
    country as country_code,
    current_timestamp as loaded_at
FROM "airflow"."public"."sample_data"