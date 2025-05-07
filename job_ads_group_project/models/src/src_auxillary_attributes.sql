with src_aux as (select * from {{ source('job_ads', 'stg_ads') }})

select experience_required, driving_license_required, access_to_own_car from src_aux