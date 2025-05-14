
with dim_job_details as (
    select * from {{ ref('src_job_details') }}
)   -- Build the dimension table for job details based on the source model

select
    {{ dbt_utils.generate_surrogate_key(['job_details_id']) }} as job_details_id,
    any_value(headline) as headline,
    any_value(description) as description,
    any_value(description_html_formatted) as description_html_formatted,
    any_value(employment_type) as employment_type,
    any_value(employment_type_concept_id) as employment_type_concept_id,
    any_value(duration) as duration,
    any_value(salary_description) as salary_description,
    any_value(application_deadline) as application_deadline,
    any_value(publication_date) as publication_date,
    any_value(vacancies) as vacancies,
    any_value(conditions) as conditions,
    any_value(application_url) as application_url,
    any_value(application_information) as application_information
from dim_job_details
group by job_details_id
