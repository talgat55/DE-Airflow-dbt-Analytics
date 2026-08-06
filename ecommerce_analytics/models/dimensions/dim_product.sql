with products as (
    select *
    from {{ ref('stg_products') }}
)
select
    product_id as product_key,
    product_id,
    product_name,
    category,
    price,
    created_at
from products