with source as (
    select * from {{ source('raw', 'raw_products') }}
)

select
    product_id,
    product_name,
    category,
    price,
    supplier,
    _loaded_at
from source
