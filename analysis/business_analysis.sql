/*
Project: Marketing Analytics Engineering Platform (V2)



SQL Engineering & Business Analysis
File: business_analysis.sql

Purpose:
Document SQL analysis supporting marketing campaign performance
evaluation and business recommendations.

Database:
PostgreSQL
Schema:
analytics

Serving tables:
- analytics.dim_campaign
- analytics.fct_campaign_performance
- analytics.campaign_metrics (computed metrics view)

Analytical conventions:
- Campaign grain: one row per campaign.
- Performance metrics are aggregated from campaign-level measures.
- Ratios are calculated from aggregated numerators and denominators
  where appropriate.
- ROAS measures revenue relative to advertising spend.
- ROI is calculated as (revenue - spend) / spend.
- Cost per conversion is used instead of CPA where the business
  meaning of "conversion" has not been independently verified.
- Findings are descriptive and do not establish causation.
*/


/* ============================================================
   1. OVERALL CAMPAIGN PERFORMANCE BASELINE

   Business question:
   What is the overall scale and performance of the campaign
   dataset available in the PostgreSQL serving layer?

   Metrics:
   - Campaign count
   - Total impressions, clicks, and conversions
   - Total advertising spend and revenue
   - Aggregate click-through rate (CTR)
   - Aggregate return on ad spend (ROAS)
   ============================================================ */

SELECT
        COUNT(*) AS campaign_rows,
        SUM(impressions) AS total_impressions,
        SUM(clicks) AS total_clicks,
        SUM(conversions) AS total_conversions,
        ROUND(SUM(spend_usd), 2) AS total_spend_usd,
        ROUND(SUM(revenue_usd), 2) AS total_revenue_usd,
        ROUND(
            SUM(clicks)::NUMERIC
            / NULLIF(SUM(impressions), 0) * 100,
            2
        ) AS aggregate_ctr_pct,
        ROUND(
            SUM(revenue_usd)::NUMERIC
            / NULLIF(SUM(spend_usd), 0),
            2
        ) AS aggregate_roas
    FROM main.fct_campaign_performance



/* ============================================================
   2. CHANNEL PERFORMANCE

   Business questions:
   - Which channels generate the most revenue?
   - Which channels have the strongest aggregate ROAS?
   - Which channels have the strongest click-through rate?
   - Which channels have the lowest cost per conversion?

   Method:
   - Join campaign attributes with campaign measures and metrics.
   - Aggregate raw measures by channel.
   - Calculate ratios from aggregated totals rather than averaging
     campaign-level ratios.
   ============================================================ */

SELECT
        d.channel,
        COUNT(*) AS campaign_count,
        SUM(f.impressions) AS total_impressions,
        SUM(f.clicks) AS total_clicks,
        SUM(f.conversions) AS total_conversions,
        ROUND(SUM(f.spend_usd), 2) AS total_spend_usd,
        ROUND(SUM(f.revenue_usd), 2) AS total_revenue_usd,
        ROUND(
            100.0 * SUM(f.clicks)
            / NULLIF(SUM(f.impressions), 0), 2
        ) AS ctr_pct,
        ROUND(
            SUM(f.spend_usd)
            / NULLIF(SUM(f.conversions), 0), 2
        ) AS cost_per_conversion_usd,
        ROUND(
            SUM(f.revenue_usd)
            / NULLIF(SUM(f.spend_usd), 0), 2
        ) AS roas
    FROM main.dim_campaign AS d
    JOIN main.fct_campaign_performance AS f
        ON d.campaign_id = f.campaign_id
    GROUP BY d.channel
    ORDER BY roas DESC, total_revenue_usd DESC


    
/* ============================================================
   3. TOP CAMPAIGNS BY REVENUE

   Business questions:
   - Which campaigns generate the most revenue?
   - What channels, regions, and product categories do they belong to?
   - How do their CTR, cost per conversion, and ROAS compare?

   Method:
   - Join campaign attributes and performance metrics.
   - Rank campaigns by revenue.
   - Return the top 10 campaigns.

   Interpretation note:
   Revenue ranking measures revenue scale, not profitability
   or marketing efficiency.
   ============================================================ */

    SELECT
        d.campaign_id,
        d.campaign_name,
        d.channel,
        d.region,
        d.product_category,
        ROUND(f.spend_usd, 2) AS spend_usd,
        ROUND(f.revenue_usd, 2) AS revenue_usd,
        ROUND(m.ctr * 100, 2) AS ctr_pct,
        ROUND(m.cpa, 2) AS cost_per_conversion_usd,
        ROUND(m.roas, 2) AS roas
    FROM main.dim_campaign AS d
    JOIN main.fct_campaign_performance AS f
        ON d.campaign_id = f.campaign_id
    JOIN main.campaign_metrics AS m
        ON f.campaign_id = m.campaign_id
    ORDER BY f.revenue_usd DESC, d.campaign_id
    LIMIT 10




/* ============================================================
   4. TOP CAMPAIGNS BY ROAS

   Business questions:
   - Which campaigns generate the highest revenue per dollar spent?
   - Which campaigns appear most efficient among those with
     meaningful advertising spend?

   Method:
   - Restrict campaigns to spend of at least $10,000.
   - Rank by campaign-level ROAS in descending order.
   - Return the top 10 campaigns.

   Important:
   The $10,000 spend threshold is an analytical screening
   condition, not an established business decision threshold.
   ROAS does not account for profit margins or other costs.
   ============================================================ */

SELECT
    d.campaign_id,
    d.campaign_name,
    d.channel,
    d.region,

    ROUND(f.spend_usd, 2) AS spend_usd,
    ROUND(f.revenue_usd, 2) AS revenue_usd,

    ROUND(m.roas, 2) AS roas,
    ROUND(m.cpa, 2) AS cost_per_conversion_usd,
    ROUND(m.ctr * 100, 2) AS ctr_pct

FROM analytics.dim_campaign AS d
JOIN analytics.fct_campaign_performance AS f
    ON d.campaign_id = f.campaign_id
JOIN analytics.campaign_metrics AS m
    ON f.campaign_id = m.campaign_id

WHERE f.spend_usd >= 10000

ORDER BY
    m.roas DESC,
    f.revenue_usd DESC,
    d.campaign_id

LIMIT 10;





/* ============================================================
   5. ROAS DISTRIBUTION AND PERFORMANCE BENCHMARKS

   Business questions:
   - What is the typical campaign-level ROAS?
   - How widely does ROAS vary across campaigns?
   - Where does the lower-performing portion of the
     campaign distribution begin?

   Method:
   - Summarize campaign-level ROAS using percentiles.
   - Report the number of campaigns meeting the $10,000
     minimum-spend screening condition.
   - Report median and maximum campaign CTR for context.

   Interpretation:
   - The median describes the middle campaign.
   - Percentiles describe the distribution, not business
     success or failure thresholds.
   - Aggregate ROAS differs from median campaign ROAS because
     aggregate ROAS is weighted by advertising spend.
   ============================================================ */

    SELECT
        COUNT(*) AS campaign_count,

        COUNT(*) FILTER (
            WHERE spend_usd >= 10000
        ) AS campaigns_spend_10k_plus,

        ROUND(MIN(roas), 2) AS min_roas,

        ROUND(
            PERCENTILE_CONT(0.25)
            WITHIN GROUP (ORDER BY roas), 2
        ) AS p25_roas,

        ROUND(
            PERCENTILE_CONT(0.50)
            WITHIN GROUP (ORDER BY roas), 2
        ) AS median_roas,

        ROUND(
            PERCENTILE_CONT(0.75)
            WITHIN GROUP (ORDER BY roas), 2
        ) AS p75_roas,

        ROUND(MAX(roas), 2) AS max_roas,

        ROUND(
            PERCENTILE_CONT(0.50)
            WITHIN GROUP (ORDER BY ctr * 100), 2
        ) AS median_ctr_pct,

        ROUND(MAX(ctr * 100), 2) AS max_ctr_pct

    FROM main.campaign_metrics


/* ============================================================
   6. LOW-ROAS CAMPAIGNS FOR INVESTIGATION

   Business questions:
   - Which campaigns have ROAS below the 25th-percentile benchmark?
   - Which of these campaigns also have at least $10,000 in spend?
   - Which campaigns should be prioritized for review?

   Method:
   - Filter campaign-level ROAS below 1.66.
   - Apply a minimum spend of $10,000.
   - Sort by lowest ROAS, then highest spend.

   Important:
   These are candidates for investigation, not automatic
   cancellation recommendations. The ROAS benchmark is based on
   this dataset's distribution, not an approved business target.
   ============================================================ */

 SELECT
        d.campaign_id,
        d.campaign_name,
        d.channel,
        d.region,
        d.product_category,
        ROUND(f.spend_usd, 2) AS spend_usd,
        ROUND(f.revenue_usd, 2) AS revenue_usd,
        ROUND(m.roas, 2) AS roas,
        ROUND(m.cpa, 2) AS cost_per_conversion_usd,
        ROUND(m.ctr * 100, 2) AS ctr_pct
    FROM main.dim_campaign AS d
    JOIN main.fct_campaign_performance AS f
        ON d.campaign_id = f.campaign_id
    JOIN main.campaign_metrics AS m
        ON f.campaign_id = m.campaign_id
    WHERE m.roas < 1.66
      AND f.spend_usd >= 10000
    ORDER BY
        m.roas ASC,
        f.spend_usd DESC,
        d.campaign_id
    LIMIT 10



/* ============================================================
   7. LOW-ROAS PERFORMANCE BY CHANNEL

   Business questions:
   - How does each channel perform within the screened
     low-ROAS campaign subset?
   - Which channels account for the most spend in this subset?
   - Which channels have the lowest aggregate ROAS here?

   Method:
   - Include campaigns with ROAS below 1.66 and spend of at
     least $10,000.
   - Aggregate spend and revenue by channel.
   - Compare aggregate ROAS with average campaign-level ROAS.

   Important:
   Results describe only the filtered subset, not the channel's
   overall performance. The thresholds are screening criteria,
   not approved business decision rules.
   ============================================================ */

SELECT
        d.channel,
        COUNT(*) AS campaign_count,
        ROUND(SUM(f.spend_usd), 2) AS total_spend_usd,
        ROUND(SUM(f.revenue_usd), 2) AS total_revenue_usd,
        ROUND(
            SUM(f.revenue_usd) / NULLIF(SUM(f.spend_usd), 0),
            2
        ) AS aggregate_roas,
        ROUND(AVG(m.roas), 2) AS avg_campaign_roas
    FROM main.dim_campaign AS d
    JOIN main.fct_campaign_performance AS f
        ON d.campaign_id = f.campaign_id
    JOIN main.campaign_metrics AS m
        ON f.campaign_id = m.campaign_id
    WHERE m.roas < 1.66
      AND f.spend_usd >= 10000
    GROUP BY d.channel
    ORDER BY
        aggregate_roas ASC,
        total_spend_usd DESC


/* ============================================================
   8. MARKETING EFFICIENCY BY CHANNEL

   Business questions:
   - Which channels have the lowest cost per click (CPC)?
   - Which channels have the lowest cost per thousand impressions
     (CPM)?
   - Which channels produce the strongest return relative to spend?

   Metrics:
   - CPC = total spend / total clicks
   - CPM = total spend / total impressions * 1,000
   - ROI = (total revenue - total spend) / total spend
   - ROAS = total revenue / total spend

   Important:
   CPC and CPM use channel-level totals rather than averages
   of campaign-level ratios.
   ROI here uses advertising spend only and should not be
   interpreted as net-profit ROI.
   ============================================================ */

    SELECT
        d.channel,
        COUNT(*) AS campaign_count,
        ROUND(
            SUM(f.spend_usd) / NULLIF(SUM(f.clicks), 0),
            2
        ) AS cpc_usd,
        ROUND(
            SUM(f.spend_usd) / NULLIF(SUM(f.impressions), 0) * 1000,
            2
        ) AS cpm_usd,
        ROUND(
            (SUM(f.revenue_usd) - SUM(f.spend_usd))
            / NULLIF(SUM(f.spend_usd), 0),
            4
        ) AS roi_ratio,
        ROUND(
            SUM(f.revenue_usd) / NULLIF(SUM(f.spend_usd), 0),
            2
        ) AS roas
    FROM main.dim_campaign AS d
    JOIN main.fct_campaign_performance AS f
        ON d.campaign_id = f.campaign_id
    GROUP BY d.channel
    ORDER BY
        roas DESC,
        cpc_usd ASC



/* ============================================================
   9. PERFORMANCE BY CAMPAIGN CHARACTERISTICS

   Business questions:
   - Which devices have the strongest aggregate ROAS?
   - Which product categories generate the strongest returns?
   - Which regions perform best on aggregate ROAS?
   - How does performance vary by target audience?

   Method:
   - Aggregate campaign measures separately for each dimension.
   - Combine the grouped results with UNION ALL.
   - Calculate ROAS and cost per conversion from aggregated
     measures, not averages of campaign-level ratios.

   Interpretation:
   These are descriptive comparisons, not causal findings.
   Each characteristic is evaluated separately.
   ============================================================ */

   WITH characteristic_performance AS (

        SELECT
            'Device' AS characteristic,
            d.device AS category,
            COUNT(*) AS campaign_count,
            SUM(f.spend_usd) AS total_spend_usd,
            SUM(f.revenue_usd) AS total_revenue_usd,
            SUM(f.conversions) AS total_conversions
        FROM main.dim_campaign AS d
        JOIN main.fct_campaign_performance AS f
            ON d.campaign_id = f.campaign_id
        GROUP BY d.device

        UNION ALL

        SELECT
            'Product Category' AS characteristic,
            d.product_category AS category,
            COUNT(*) AS campaign_count,
            SUM(f.spend_usd) AS total_spend_usd,
            SUM(f.revenue_usd) AS total_revenue_usd,
            SUM(f.conversions) AS total_conversions
        FROM main.dim_campaign AS d
        JOIN main.fct_campaign_performance AS f
            ON d.campaign_id = f.campaign_id
        GROUP BY d.product_category

        UNION ALL

        SELECT
            'Region' AS characteristic,
            d.region AS category,
            COUNT(*) AS campaign_count,
            SUM(f.spend_usd) AS total_spend_usd,
            SUM(f.revenue_usd) AS total_revenue_usd,
            SUM(f.conversions) AS total_conversions
        FROM main.dim_campaign AS d
        JOIN main.fct_campaign_performance AS f
            ON d.campaign_id = f.campaign_id
        GROUP BY d.region

        UNION ALL

        SELECT
            'Target Audience' AS characteristic,
            d.target_audience AS category,
            COUNT(*) AS campaign_count,
            SUM(f.spend_usd) AS total_spend_usd,
            SUM(f.revenue_usd) AS total_revenue_usd,
            SUM(f.conversions) AS total_conversions
        FROM main.dim_campaign AS d
        JOIN main.fct_campaign_performance AS f
            ON d.campaign_id = f.campaign_id
        GROUP BY d.target_audience
    )

    SELECT
        characteristic,
        category,
        campaign_count,
        ROUND(total_spend_usd, 2) AS total_spend_usd,
        ROUND(total_revenue_usd, 2) AS total_revenue_usd,
        ROUND(
            total_revenue_usd / NULLIF(total_spend_usd, 0),
            2
        ) AS aggregate_roas,
        ROUND(
            total_spend_usd / NULLIF(total_conversions, 0),
            2
        ) AS cost_per_conversion_usd
    FROM characteristic_performance
    ORDER BY
        characteristic,
        aggregate_roas DESC,
        category

/* ============================================================
   10. ANALYSIS SCOPE AND LIMITATIONS

   Scope:
   - Descriptive analysis of campaign-level marketing measures.
   - Channel, campaign, efficiency, and campaign-characteristic
     comparisons using PostgreSQL serving tables.

   Metric definitions:
   - CTR = clicks / impressions
   - Cost per conversion = spend / conversions
   - CPC = spend / clicks
   - CPM = spend / impressions * 1,000
   - ROAS = revenue / spend
   - ROI ratio = (revenue - spend) / spend

   Limitations:
   - ROI uses advertising spend only; it is not net-profit ROI.
   - ROAS does not account for profit margins or other costs.
   - The $10,000 spend filter and 1.66 ROAS benchmark are
     analytical screening criteria, not approved business rules.
   - Campaign-level findings are descriptive and do not establish
     causal relationships.
   - Source measures were reconstructed in the upstream modeling
     process. Their business semantics should be validated before
     operational budget decisions.
   - PostgreSQL serving tables require an explicit refresh from
     the upstream DuckDB/dbt workflow; running dbt alone does not
     automatically refresh the PostgreSQL serving layer.
   ============================================================ */