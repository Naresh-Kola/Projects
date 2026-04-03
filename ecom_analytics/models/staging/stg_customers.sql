with source as (
    select * from {{ source('raw', 'raw_customers') }}
)

select
    customer_id,
    first_name,
    last_name,
    first_name || ' ' || last_name as full_name,
    email,
    signup_date,
    country,
    _loaded_at
from source
