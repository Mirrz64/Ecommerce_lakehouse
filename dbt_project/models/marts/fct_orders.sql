{{ config(materialized='table') }}

with orders as (
    select * from {{ ref('int_cleaned_orders') }}
)

select
    order_id,
    customer_id,
    order_amount_usd,
    order_status,
    ordered_at,
    is_high_value_transaction,
    current_timestamp as dbt_transformed_at

from orders