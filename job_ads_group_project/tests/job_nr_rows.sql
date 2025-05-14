with fct as(
    select count(distinct job_details_id) as nr_rows_fct
    from {{ ref('fct_job_ads') }}
),

dim as(
	select count(*) as nr_rows_dim
	from {{ ref('dim_job_details') }}
),

comparison as (
	select *
	from fct
	cross join dim
)

select * from comparison