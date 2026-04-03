with source as (
    select * from {{ source('raw', 'raw_order_items') }}
)

select
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    quantity * unit_price as line_total,
    _loaded_at
from source
