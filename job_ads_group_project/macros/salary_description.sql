{% macro salary_description(column_name) %}
    CASE 
        WHEN {{ column_name }} = 'Fast l?n' THEN 'Fast lön'
        ELSE {{ column_name }}
    END
{% endmacro %}