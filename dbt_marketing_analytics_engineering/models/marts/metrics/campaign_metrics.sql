with base as (

    select
        campaign_id,
        impressions,
        clicks,
        conversions,
        spend_usd,
        revenue_usd

    from {{ ref('fct_campaign_performance') }}

),

metrics as (

    select
        campaign_id,
        impressions,
        clicks,
        conversions,
        spend_usd,
        revenue_usd,

case
    when impressions > 0
    then clicks * 1.0 / impressions
    else null
end as ctr,

case
    when conversions > 0
    then spend_usd * 1.0 / conversions
    else null
end as cpa,

case
    when clicks > 0
    then spend_usd * 1.0 / clicks
    else null
end as cpc,

case
    when impressions > 0
    then spend_usd * 1.0 / impressions * 1000
    else null
end as cpm,

case
    when spend_usd > 0
    then (revenue_usd - spend_usd) * 1.0 / spend_usd
    else null
end as roi,

case
    when spend_usd > 0
    then revenue_usd * 1.0 / spend_usd
    else null
end as roas



    from base

)

select *
from metrics