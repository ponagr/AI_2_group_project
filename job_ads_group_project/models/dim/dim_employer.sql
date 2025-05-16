with dim_employer as (select * from {{ ref('src_employer') }})

select
    {{ dbt_utils.generate_surrogate_key(['employer_workplace', 'workplace_city']) }} as employer_id,
    coalesce(any_value(employer_name), 'Ej Angiven') as employer_name,
    coalesce(employer_workplace, 'Ej Angiven') as employer_workplace,
    coalesce(any_value(employer_organization_number), 'Ej Angiven') as employer_organization_number,
    coalesce(any_value(workplace_country), 'Ej Angiven') as workplace_country,
    coalesce(any_value(workplace_region), 'Ej Angiven') as workplace_region,
    coalesce(workplace_city, 'Ej Angiven') as workplace_city,
    coalesce(any_value(workplace_street_address), 'Ej Angiven') as workplace_street_address,
    coalesce(any_value(workplace_postcode), 'Ej Angiven') as workplace_postcode
from dim_employer
group by employer_workplace, workplace_city