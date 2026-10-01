-- Singular Tests 1/ it seems singular test doesnt mean just a single test taken after all : ) 


select
    campaign_id
from {{ ref('int_campaign_performance') }}
where
    clicks > impressions
    or conversions > clicks

-- Show me campaigns where the business rule is violated

-- Return any campaign that violates the expected measure relationship

