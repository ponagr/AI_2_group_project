
with job_details as (
    select * from {{ ref('src_job_details') }}
)

select 
    {{dbt_utils.generate_surrogate_key(['id'])}} as job_details_id,
    coalesce(headline, 'Ej Angiven') as headline,
    coalesce(description, 'Ej Angiven') as description,
    coalesce(description_html, 'Ej Angiven') as description_html,
    coalesce(employment_type, 'Ej Angiven') as employment_type,
    coalesce(duration, 'Ej Angiven') as duration,
    coalesce(salary_type, 'Ej Angiven') as salary_type,
    coalesce(salary_description, 'Ej Angiven') as salary_description,
    coalesce(working_hours_type, 'Ej Angiven') as working_hours_type,
    scope_of_work_min,
    scope_of_work_max
from job_details