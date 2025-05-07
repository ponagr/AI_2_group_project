with src_license as (select * from {{ source('job_ads', 'stg_driving_license') }})

select * from src_license