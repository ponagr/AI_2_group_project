with dim_employer as (select * from {{ ref('src_employer') }})

select
    {{ dbt_utils.generate_surrogate_key(['employer_workplace', 'workplace_city']) }} as employer_id,
    any_value(employer_name) as employer_name,
    employer_workplace,
    any_value(employer_organization_number) as employer_organization_number,
    any_value(workplace_country)as workplace_country,
    any_value(workplace_region) as workplace_region,
    workplace_city,
    any_value(workplace_street_address) as workplace_street_address,
    any_value(workplace_postcode) as workplace_postcode
from dim_employer
group by employer_workplace, workplace_city