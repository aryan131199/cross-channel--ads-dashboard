-- ============================================================
-- Step 2: Unified cross-channel marketing table (BigQuery)
-- Normalises all three platforms into a single schema.
-- Computed KPIs: ctr, cpc, cpa, conversion_rate
-- Platform-exclusive columns kept; NULL where not applicable.
-- ============================================================

CREATE OR REPLACE TABLE `marketing_analytics.unified_ads` AS

-- ── Facebook ──────────────────────────────────────────────────
SELECT
  date,
  'Facebook'                                          AS platform,
  campaign_id,
  campaign_name,
  ad_set_id                                           AS ad_group_id,
  ad_set_name                                         AS ad_group_name,
  impressions,
  clicks,
  spend,
  conversions,

  -- Computed KPIs
  SAFE_DIVIDE(clicks, impressions)                    AS ctr,
  SAFE_DIVIDE(spend, clicks)                          AS cpc,
  SAFE_DIVIDE(spend, conversions)                     AS cpa,
  SAFE_DIVIDE(conversions, clicks)                    AS conversion_rate,

  -- Platform-specific: Facebook
  video_views,
  reach,
  frequency,
  engagement_rate,

  -- Platform-specific: Google (null)
  NULL                                                AS conversion_value,
  NULL                                                AS quality_score,
  NULL                                                AS search_impression_share,

  -- Platform-specific: TikTok (null)
  NULL                                                AS video_watch_25_pct,
  NULL                                                AS video_watch_50_pct,
  NULL                                                AS video_watch_75_pct,
  NULL                                                AS video_watch_100_pct,
  NULL                                                AS likes,
  NULL                                                AS shares,
  NULL                                                AS comments

FROM `marketing_analytics.facebook_ads`

UNION ALL

-- ── Google ────────────────────────────────────────────────────
SELECT
  date,
  'Google'                                            AS platform,
  campaign_id,
  campaign_name,
  ad_group_id,
  ad_group_name,
  impressions,
  clicks,
  cost                                                AS spend,
  conversions,

  SAFE_DIVIDE(clicks, impressions)                    AS ctr,
  SAFE_DIVIDE(cost, clicks)                           AS cpc,
  SAFE_DIVIDE(cost, conversions)                      AS cpa,
  SAFE_DIVIDE(conversions, clicks)                    AS conversion_rate,

  -- Facebook-specific (null)
  NULL                                                AS video_views,
  NULL                                                AS reach,
  NULL                                                AS frequency,
  NULL                                                AS engagement_rate,

  -- Google-specific
  conversion_value,
  quality_score,
  search_impression_share,

  -- TikTok-specific (null)
  NULL                                                AS video_watch_25_pct,
  NULL                                                AS video_watch_50_pct,
  NULL                                                AS video_watch_75_pct,
  NULL                                                AS video_watch_100_pct,
  NULL                                                AS likes,
  NULL                                                AS shares,
  NULL                                                AS comments

FROM `marketing_analytics.google_ads`

UNION ALL

-- ── TikTok ────────────────────────────────────────────────────
SELECT
  date,
  'TikTok'                                            AS platform,
  campaign_id,
  campaign_name,
  adgroup_id                                          AS ad_group_id,
  adgroup_name                                        AS ad_group_name,
  impressions,
  clicks,
  cost                                                AS spend,
  conversions,

  SAFE_DIVIDE(clicks, impressions)                    AS ctr,
  SAFE_DIVIDE(cost, clicks)                           AS cpc,
  SAFE_DIVIDE(cost, conversions)                      AS cpa,
  SAFE_DIVIDE(conversions, clicks)                    AS conversion_rate,

  -- Facebook-specific (null)
  video_views,
  NULL                                                AS reach,
  NULL                                                AS frequency,
  NULL                                                AS engagement_rate,

  -- Google-specific (null)
  NULL                                                AS conversion_value,
  NULL                                                AS quality_score,
  NULL                                                AS search_impression_share,

  -- TikTok-specific: store as completion % of total impressions
  SAFE_DIVIDE(video_watch_25,  impressions)           AS video_watch_25_pct,
  SAFE_DIVIDE(video_watch_50,  impressions)           AS video_watch_50_pct,
  SAFE_DIVIDE(video_watch_75,  impressions)           AS video_watch_75_pct,
  SAFE_DIVIDE(video_watch_100, impressions)           AS video_watch_100_pct,
  likes,
  shares,
  comments

FROM `marketing_analytics.tiktok_ads`
;
