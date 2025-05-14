

with stg_ads as (
    select * from {{ source('job_ads', 'stg_ads') }}
)  -- loading raw job details data from the source table


-- Select relevant fields for the src_job_details model
-- Renaming columns to match dimensional model naming conventions
select
    id as job_details_id,
    headline,
    description__text as description,
    description__text_formatted as description_html_formatted,
    employment_type__label as employment_type,
    employment_type__concept_id as employment_type_concept_id,
    duration__label as duration,
    salary_description,
    application_deadline,
    publication_date,
    number_of_vacancies as vacancies,
    description__conditions as conditions,
    application_details__url as application_url,
    application_details__information as application_information
from stg_ads
where headline is not null

