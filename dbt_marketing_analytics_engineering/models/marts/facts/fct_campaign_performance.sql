-- fct Table: fct_campaign_performance

select
    campaign_id,
    impressions,
    clicks,
    conversions,
    spend_usd,
    revenue_usd

from {{ ref('int_campaign_performance') }}