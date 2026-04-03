with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select
        order_id,
        count(*) as item_count,
        sum(line_total) as items_total
    from {{ ref('stg_order_items') }}
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.total_amount,
    coalesce(oi.item_count, 0) as item_count,
    coalesce(oi.items_total, 0) as items_total
from orders o
left join order_items oi on o.order_id = oi.order_id
