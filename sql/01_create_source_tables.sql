-- ============================================================
-- Step 1: Create source tables (BigQuery)
-- Upload each CSV to a dataset named `marketing_analytics`
-- ============================================================

-- ── Facebook Ads ─────────────────────────────────────────────
CREATE OR REPLACE TABLE `marketing_analytics.facebook_ads` (
  date              DATE,
  campaign_id       STRING,
  campaign_name     STRING,
  ad_set_id         STRING,
  ad_set_name       STRING,
  impressions       INT64,
  clicks            INT64,
  spend             FLOAT64,
  conversions       INT64,
  video_views       INT64,
  engagement_rate   FLOAT64,
  reach             INT64,
  frequency         FLOAT64
);

-- ── Google Ads ────────────────────────────────────────────────
CREATE OR REPLACE TABLE `marketing_analytics.google_ads` (
  date                      DATE,
  campaign_id               STRING,
  campaign_name             STRING,
  ad_group_id               STRING,
  ad_group_name             STRING,
  impressions               INT64,
  clicks                    INT64,
  cost                      FLOAT64,
  conversions               INT64,
  conversion_value          FLOAT64,
  ctr                       FLOAT64,
  avg_cpc                   FLOAT64,
  quality_score             INT64,
  search_impression_share   FLOAT64
);

-- ── TikTok Ads ────────────────────────────────────────────────
CREATE OR REPLACE TABLE `marketing_analytics.tiktok_ads` (
  date              DATE,
  campaign_id       STRING,
  campaign_name     STRING,
  adgroup_id        STRING,
  adgroup_name      STRING,
  impressions       INT64,
  clicks            INT64,
  cost              FLOAT64,
  conversions       INT64,
  video_views       INT64,
  video_watch_25    INT64,
  video_watch_50    INT64,
  video_watch_75    INT64,
  video_watch_100   INT64,
  likes             INT64,
  shares            INT64,
  comments          INT64
);
