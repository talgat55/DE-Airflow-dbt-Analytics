with sales as (
    select *
    from {{ ref('fact_order_items') }}
),
customers as (
    select *
    from {{ ref('dim_customer') }}
),

customer_ltv as (
    select
        c.customer_key,
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        c.country,
        c.city,

        count(distinct s.order_id) as orders_count,
        sum(s.quantity) as items_bought,
        round(sum(s.line_total), 2) as lifetime_value,
        min(s.order_created_at) as first_order_at,
        max(s.order_created_at) as last_order_at

    from sales s
    inner join customers c
        on s.customer_key = c.customer_key
    where s.order_status != 'cancelled'
    group by
        c.customer_key,
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        c.country,
        c.city
)

select *
from customer_ltv