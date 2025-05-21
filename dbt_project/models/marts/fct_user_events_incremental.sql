{{
    config(
        materialized='incremental',
        unique_key='event_id',
        incremental_strategy='merge'
    )
}}

SELECT
    event_id,
    user_id,
    event_type,
    event_timestamp,
    page_url,
    session_id,
    CURRENT_TIMESTAMP as processed_at
FROM {{ source('raw', 'user_events') }}

{% if is_incremental() %}
    -- This is a common interview question: how to handle incremental loads
    WHERE event_timestamp > (
        SELECT MAX(event_timestamp)
        FROM {{ this }}
    )
{% endif %} 