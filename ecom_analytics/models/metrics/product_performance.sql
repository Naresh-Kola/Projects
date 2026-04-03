with product_stats as (
    select
        product_id,
        product_name,
        category,
        total_units_sold,
        total_revenue
    from {{ ref('dim_products') }}
)

select
    product_id,
    product_name,
    category,
    total_units_sold,
    total_revenue,
    rank() over (order by total_revenue desc) as revenue_rank
from product_stats
order by revenue_rank
