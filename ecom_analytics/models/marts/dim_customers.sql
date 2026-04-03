with customer_orders as (
    select * from {{ ref('int_customer_orders') }}
)

select
    customer_id,
    full_name,
    email,
    country,
    signup_date,
    total_orders,
    total_spent,
    tenure_days,
    case
        when total_spent >= 500 then 'Gold'
        when total_spent >= 200 then 'Silver'
        else 'Bronze'
    end as customer_tier
from customer_orders
