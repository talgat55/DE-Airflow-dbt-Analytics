with source_data as (

    select *
    from {{ source('raw', 'orders') }}

),

cleaned as (

    select
        order_id,
        customer_id,
        lower(trim(order_status)) as order_status,
        order_created_at
    from source_data
    where order_id is not null
      and customer_id is not null
      and lower(trim(order_status)) in (
          'created',
          'paid',
          'shipped',
          'delivered',
          'cancelled'
      )

)

select *
from cleaned