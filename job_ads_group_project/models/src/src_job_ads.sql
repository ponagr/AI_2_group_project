with job_ads as (select * from {{ source('job_ads', 'stg_ads') }})

select * from job_ads