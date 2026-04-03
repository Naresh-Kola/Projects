with customers as (
    select * from {{ ref('dim_customers') }}
    where tenure_days > 0
)

select
    customer_id,
    full_name,
    email,
    country,
    customer_tier,
    total_orders,
    total_spent,
    tenure_days,
    round(total_spent / tenure_days * 365, 2) as projected_annual_value
from customers
