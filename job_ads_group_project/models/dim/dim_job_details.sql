
with job_details as (
    select * from {{ ref('src_job_details') }}
)

select
    job_details_id,
    headline,
    description,
    employment_type,
    duration,
    salary_type,
    scope_of_work_min,
    scope_of_work_max,
    working_hours_type,

from job_details
