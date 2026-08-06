with sales as (
    select *
    from {{ ref('fact_order_items') }}
),

daily_sales as (
    select
        order_created_at::date as sales_date,
        count(distinct order_id) as orders_count,
        count(*) as order_items_count,
        sum(quantity) as items_sold,
        round(sum(line_total), 2) as revenue,
        round(
            sum(line_total)
            / nullif(count(distinct order_id), 0),
            2
        ) as average_order_value
    from sales
    where order_status != 'cancelled'
    group by order_created_at::date
)

select *
from daily_sales