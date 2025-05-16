{% test mart_row_count_match(model) %}

    with fct as(
        select count(*) as nr_rows_fct
        from {{ ref('fct_job_ads') }}
    ),

    mart as(
        select count(*) as nr_rows_mart
        from {{ ref('mart_full_job_ads') }}
    ),

    src as(
        select count(*) as nr_rows_src
        from {{ ref('src_job_ads') }}
    ),

    comparison as (
        select *
        from fct
        cross join mart
        cross join src
    )

    select *
    from comparison
    where nr_rows_fct != nr_rows_mart or nr_rows_mart != nr_rows_src

{% endtest %}