with source_data as (
    select *
    from {{source('raw', 'customers')}}
),
cleaned as (
    select
        customer_id,
        initcap(trim(first_name)) as first_name,
        initcap(trim(last_name)) as last_name,
        lower(trim(email)) as email,
        nullif(trim(country), '') as country,
        nullif(trim(city), '') as city,
        registered_at
    from source_data
    where customer_id is not null
        and email is not null
)

select *
from cleaned