{% test positive_values(model, column_name, zero_allowed=false) %}

-- Common interview question: implement a custom test
WITH validation AS (
    SELECT
        {{ column_name }} as value
    FROM {{ model }}
    WHERE {{ column_name }} is not null
        {% if not zero_allowed %}
            AND {{ column_name }} <= 0
        {% else %}
            AND {{ column_name }} < 0
        {% endif %}
)

SELECT *
FROM validation

{% endtest %} 