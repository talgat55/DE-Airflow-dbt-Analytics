with source_data as (
    select *
    from {{ source('raw', 'payments') }}
),
cleaned as (
    select
        payment_id,
        order_id,
        lower(trim(payment_method)) as payment_method,
        lower(trim(payment_status)) as payment_status,
        amount,
        paid_at
    from source_data
    where payment_id is not null
      and order_id is not null
      and amount >= 0
)

select *
from cleaned