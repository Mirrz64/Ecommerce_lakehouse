{{ config(materialized='table') }}

with customers as (
    select * from {{ ref('int_cleaned_customers') }}
),

orders as (
    select * from {{ ref('int_cleaned_orders') }}
),

-- Aggregate transaction behaviors per customer profile
customer_orders_summary as (
    select
        customer_id,
        count(order_id) as total_orders_placed,
        coalesce(sum(order_amount_usd), 0) as lifetime_spend_usd,
        min(ordered_at) as first_order_date
    from orders
    where order_status = 'completed'
    group by customer_id
)

select
    c.customer_id,
    c.full_name,
    c.customer_email,
    c.registered_at,
    coalesce(s.total_orders_placed, 0) as total_orders_placed,
    coalesce(s.lifetime_spend_usd, 0) as lifetime_spend_usd,
    s.first_order_date

from customers c
left join customer_orders_summary s on c.customer_id = s.customer_id