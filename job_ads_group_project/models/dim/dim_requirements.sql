with jobs as (select * from {{ ref('src_job_ads') }}),


ski as (
    select
        _dlt_parent_id,
        string_agg(label) as required_skills
    from {{ ref('src_must_skills') }}
    group by _dlt_parent_id
),


lic as (
    select 
        _dlt_parent_id,
        string_agg(label) as required_license
    from {{ ref('src_driving_license') }}
    group by _dlt_parent_id
),


final as (
    select 
        {{dbt_utils.generate_surrogate_key(['j._dlt_id'])}} as job_requirements_id,
        j._dlt_id,
        lic.required_license,
        ski.required_skills
    from jobs j
    left join ski on ski._dlt_parent_id = j._dlt_id
    left join lic on lic._dlt_parent_id = j._dlt_id
)

select * from final
