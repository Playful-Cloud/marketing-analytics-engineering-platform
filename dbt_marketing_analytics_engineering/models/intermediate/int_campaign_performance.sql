    -- Int

    with base as (

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

        from {{ ref('stg_campaign_performance') }}

    ),

    corrected as (

        select
            campaign_id,
            campaign_name,
            start_date,
            end_date,
            channel,
            region,

            greatest(impressions, clicks, conversions) as impressions,

            impressions
                + clicks
                + conversions
                - greatest(impressions, clicks, conversions)
                - least(impressions, clicks, conversions) as clicks,

            least(impressions, clicks, conversions) as conversions,

            spend_usd,
            revenue_usd,
            target_audience,
            product_category,
            device,
            year

        from base

    )

    select *
    from corrected