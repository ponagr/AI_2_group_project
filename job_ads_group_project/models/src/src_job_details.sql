-- models/src/src_job_details.sql

with stg_job_details as (
    select * from {{ source('job_ads', 'stg_job_details') }}
)

select
    job_details_id,
    headline,
    description,
    description_html_formatted,
    employment_type,
    duration,
    salary_type,
    scope_of_work_min,
    scope_of_work_max
from stg_job_details
