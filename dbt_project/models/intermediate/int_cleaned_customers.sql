{{ config(materialized='ephemeral') }}

with staged_customers as (
    select * from {{ ref('stg_customers') }}
)

select
    customer_id,
    customer_email,
    registered_at,
    -- Combine name fields cleanly for BI tool usage
    initcap(first_name || ' ' || last_name) as full_name

from staged_customers