with source_data as (
    select *
    from {{ source('raw', 'order_items') }}

),

cleaned as (
    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        round(quantity * unit_price, 2) as line_total
    from source_data
    where order_item_id is not null
      and order_id is not null
      and product_id is not null
      and quantity > 0
      and unit_price >= 0

)

select *
from cleaned