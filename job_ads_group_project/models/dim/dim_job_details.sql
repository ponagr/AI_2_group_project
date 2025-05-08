-- models/dim/dim_job_details.sql

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

    case
        when scope_of_work_max > 100 then 'Full-time'
        when scope_of_work_max between 50 and 100 then 'Part-time'
        else 'Other'
    end as work_scope_category

from job_details
where headline is not null
