{{ config(materialized='view') }}

with source_data as (
    select * from {{ source('raw_source', 'customers') }}
)

select
    customer_id,
    lower(trim(first_name)) as first_name,
    lower(trim(last_name)) as last_name,
    lower(trim(email)) as customer_email,
    cast(created_at as timestamp) as registered_at

from source_data