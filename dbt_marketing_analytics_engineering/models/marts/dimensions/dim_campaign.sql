-- Dim CAmpaigbn Table


select
    campaign_id,
    campaign_name,
    start_date,
    end_date,
    channel,
    region,
    target_audience,
    product_category,
    device,
    year

from {{ ref('int_campaign_performance') }}