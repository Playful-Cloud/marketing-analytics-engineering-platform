select
    campaign_id,
    campaign_name,
    start_date,
    end_date,
    channel,
    region,
    impressions,
    clicks,
    conversions,
    spend_usd,
    revenue_usd,
    target_audience,
    product_category,
    device,
    year

from {{ source('marketing', 'marketing_campaign') }}