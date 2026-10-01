--singular test 2/ i think its better to call this custom test after all

select
    campaign_id
from {{ ref('int_campaign_performance') }}
where
    impressions < 0
    or clicks < 0
    or conversions < 0
    or spend_usd < 0
    or revenue_usd < 0


-- Show me any campaign containing a negative measur