with order_items as (
    select *
    from {{ ref('stg_order_items') }}
),
orders as (
    select *
    from {{ ref('stg_orders') }}
),
payments as (
    select *
    from {{ ref('stg_payments') }}
),
customers as (
    select *
    from {{ ref('dim_customer') }}
),
products as (
    select *
    from {{ ref('dim_product') }}
),
final as (
    select
        oi.order_item_id,
        oi.order_id,

        c.customer_key,
        p.product_key,

        o.order_status,
        o.order_created_at,

        pay.payment_method,
        pay.payment_status,
        pay.paid_at,

        oi.quantity,
        oi.unit_price,
        oi.line_total

    from order_items oi

    inner join orders o
        on oi.order_id = o.order_id

    inner join customers c
        on o.customer_id = c.customer_id

    inner join products p
        on oi.product_id = p.product_id

    left join payments pay
        on oi.order_id = pay.order_id

)

select *
from final