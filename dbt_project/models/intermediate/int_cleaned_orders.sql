{{ config(materialized='ephemeral') }}

with staged_orders as (
    select * from {{ ref('stg_orders') }}
)

select
    order_id,
    customer_id,
    order_amount_usd,
    order_status,
    ordered_at,
    case 
        when order_amount_usd >= 150.00 then true 
        else false 
    end as is_high_value_transaction

from staged_orders