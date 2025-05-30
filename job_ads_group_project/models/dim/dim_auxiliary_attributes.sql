with dim_aux as (select * from {{ ref('src_auxiliary_attributes') }})

select
    {{dbt_utils.generate_surrogate_key(['experience_required', 'driving_license_required', 'access_to_own_car'])}} as auxiliary_attributes_id,
    max(experience_required) as experience_required, 
    max(driving_license_required) as driver_license, 
    max(access_to_own_car) as access_to_own_car
from dim_aux
group by auxiliary_attributes_id