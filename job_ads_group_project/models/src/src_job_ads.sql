with job_ads as (select * from {{ source('job_ads', 'stg_ads') }})

select 
    id,
    _dlt_id,
    occupation__label,
    employer__workplace,
    workplace_address__municipality,
    experience_required,
    driving_license_required,
    access_to_own_car,
    number_of_vacancies,
    relevance,
    publication_date,
    application_deadline
from job_ads