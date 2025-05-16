with job_details as (
    select * from {{ ref('src_job_details') }}
)   -- Build the dimension table for job details based on the source model

select
    {{ dbt_utils.generate_surrogate_key(['id']) }} as job_details_id,
    headline,
    description,
    description_html,
    employment_type,
    coalesce(duration, 'ej angiven') as duration,
    salary_type,
    salary_description,
    working_hours_type,
    scope_of_work_min,
    scope_of_work_max,
    publication_date
from job_details
