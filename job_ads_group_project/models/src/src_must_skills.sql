with src_skills as (select * from {{ source('job_ads', 'stg_must_skills') }})

select * from src_skills