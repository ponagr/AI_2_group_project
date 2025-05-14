with fct as(
    select count(distinct auxillary_attributes_id) as nr_rows_fct
    from {{ ref('fct_job_ads') }}
),

dim as(
	select count(*) as nr_rows_dim
	from {{ ref('dim_auxillary_attributes') }}
),

comparison as (
	select *
	from fct
	cross join dim
)

select * from comparison