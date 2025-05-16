with job_ads as (select * from {{ ref('mart_full_job_ads') }})


select 
    occupation_group,
    occupation,
    headline,
    employer_name,
    description,
    duration,
    salary_type,
    salary_description,
    working_hours_type,
    employer_workplace,
    employer_organization_number,
    workplace_country,
    workplace_region,
    workplace_city,
    workplace_street_address,
    workplace_postcode,
    required_license,
    required_skills,
    description_html,
    scope_of_work_min,
    scope_of_work_max,
    vacancies,
    relevance,
    application_deadline,
    experience_required,
    driver_license,
    access_to_own_car,
    publication_date
from job_ads j
where occupation_field = 'Transport, distribution, lager'