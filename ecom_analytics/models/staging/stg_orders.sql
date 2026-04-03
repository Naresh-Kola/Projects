with source as (
    select * from {{ source('raw', 'raw_orders') }}
)

select
    order_id,
    customer_id,
    order_date,
    status,
    total_amount,
    _loaded_at
from source
