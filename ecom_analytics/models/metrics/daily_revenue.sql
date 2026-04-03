with orders as (
    select * from {{ ref('fct_orders') }}
    where status != 'cancelled'
)

select
    order_date::date as revenue_date,
    count(order_id) as total_orders,
    sum(total_amount) as daily_revenue
from orders
group by order_date::date
order by revenue_date
