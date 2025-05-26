with stg_ads as (
    select * from {{ source('job_ads', 'stg_ads') }}
)  -- loading raw job details data from the source table


-- Select relevant fields for the src_job_details model
-- Renaming columns to match dimensional model naming conventions
select
    id,
    headline,
    description__text as description,
    description__text_formatted as description_html,
    employment_type__label as employment_type,
    duration__label as duration,
    salary_description,
    salary_type__label as salary_type,
    scope_of_work__min as scope_of_work_min,
    scope_of_work__max as scope_of_work_max,
    working_hours_type__label as working_hours_type
from stg_ads
