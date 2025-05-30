with job_ads as (select * from {{ ref('fct_job_ads') }})

select 
    occupation_field,
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
    CAST(application_deadline AS DATE) as application_deadline,
    experience_required,
    driver_license,
    access_to_own_car,
    CAST(publication_date AS DATE) as publication_date
from job_ads j
left join {{ ref('dim_auxiliary_attributes') }} a on a.auxiliary_attributes_id = j.auxiliary_attributes_id
left join {{ ref('dim_occupation') }} o on o.occupation_id = j.occupation_id
left join {{ ref('dim_job_details') }} jd on jd.job_details_id = j.job_details_id
left join {{ ref('dim_employer') }} e on e.employer_id = j.employer_id
left join {{ ref('dim_requirements') }} r on r.job_requirements_id = j.job_requirements_id