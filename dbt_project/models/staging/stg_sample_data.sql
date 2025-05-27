{{
    config(
        materialized='view',
        tags=['staging']
    )
}}

SELECT
    id::integer as user_id,
    name as full_name,
    country as country_code,
    current_timestamp as loaded_at
FROM {{ ref('sample_data') }} 