{{ config(materialized='view') }}

with source_data as (
    select * from {{ source('raw_source', 'orders') }}
)

select
    order_id,
    customer_id,
    order_amount as order_amount_usd,
    lower(order_status) as order_status,
    cast(order_date as timestamp) as ordered_at

from source_data