with source_data as (
    select *
    from {{ source('raw', 'products')}}
),
cleaned as (
    select
        product_id,
        initcap(trim(product_name)) as product_name,
        initcap(trim(category)) as category,
        price,
        created_at
    from source_data
    where product_id is not null
        and price >= 0
)

select *
from cleaned