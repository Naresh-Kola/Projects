with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
)

select
    c.customer_id,
    c.full_name,
    c.email,
    c.country,
    c.signup_date,
    count(o.order_id) as total_orders,
    coalesce(sum(o.total_amount), 0) as total_spent,
    datediff('day', c.signup_date, current_date()) as tenure_days
from customers c
left join orders o on c.customer_id = o.customer_id
group by
    c.customer_id,
    c.full_name,
    c.email,
    c.country,
    c.signup_date
