with sales as (
    select *
    from {{ ref('fact_order_items') }}
),
products as (
    select *
    from {{ ref('dim_product') }}
),
product_performance as (
    select
        p.product_key,
        p.product_id,
        p.product_name,
        p.category,

        count(distinct s.order_id) as orders_count,
        sum(s.quantity) as quantity_sold,
        round(sum(s.line_total), 2) as revenue,
        round(avg(s.unit_price), 2) as average_selling_price

    from sales s
    inner join products p
        on s.product_key = p.product_key
    where s.order_status != 'cancelled'
    group by
        p.product_key,
        p.product_id,
        p.product_name,
        p.category
)

select *
from product_performance