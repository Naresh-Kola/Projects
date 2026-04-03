with products as (
    select * from {{ ref('stg_products') }}
),

product_metrics as (
    select
        product_id,
        sum(quantity) as total_units_sold,
        sum(line_total) as total_revenue
    from {{ ref('int_order_items_enriched') }}
    group by product_id
)

select
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    p.supplier,
    coalesce(pm.total_units_sold, 0) as total_units_sold,
    coalesce(pm.total_revenue, 0) as total_revenue
from products p
left join product_metrics pm on p.product_id = pm.product_id
