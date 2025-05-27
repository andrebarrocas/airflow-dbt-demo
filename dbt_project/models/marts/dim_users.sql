{{
    config(
        materialized='table',
        tags=['mart']
    )
}}

WITH source AS (
    SELECT * FROM {{ ref('stg_sample_data') }}
),

final AS (
    SELECT
        user_id,
        full_name,
        country_code,
        -- Add some derived fields
        CASE 
            WHEN country_code = 'USA' THEN 'North America'
            WHEN country_code = 'Canada' THEN 'North America'
            WHEN country_code = 'UK' THEN 'Europe'
            ELSE 'Other'
        END as region,
        loaded_at,
        current_timestamp as transformed_at
    FROM source
)

SELECT * FROM final 