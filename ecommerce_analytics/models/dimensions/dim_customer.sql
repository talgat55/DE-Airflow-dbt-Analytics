with customers as (
    select *
    from {{ ref('stg_customers') }}

)
select
    customer_id as customer_key,
    customer_id,
    first_name,
    last_name,
    email,
    country,
    city,
    registered_at
from customers