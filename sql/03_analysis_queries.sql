-- ============================================================
-- Step 3: Analysis queries on the unified table
-- ============================================================

-- ── 1. Overall KPI summary by platform ───────────────────────
SELECT
  platform,
  SUM(spend)                                          AS total_spend,
  SUM(impressions)                                    AS total_impressions,
  SUM(clicks)                                         AS total_clicks,
  SUM(conversions)                                    AS total_conversions,
  ROUND(SAFE_DIVIDE(SUM(clicks), SUM(impressions)) * 100, 2)  AS ctr_pct,
  ROUND(SAFE_DIVIDE(SUM(spend),  SUM(clicks)), 2)             AS avg_cpc,
  ROUND(SAFE_DIVIDE(SUM(spend),  SUM(conversions)), 2)        AS avg_cpa
FROM `marketing_analytics.unified_ads`
GROUP BY platform
ORDER BY total_spend DESC;


-- ── 2. Daily spend trend per platform ────────────────────────
SELECT
  date,
  platform,
  ROUND(SUM(spend), 2)  AS daily_spend,
  SUM(conversions)      AS daily_conversions
FROM `marketing_analytics.unified_ads`
GROUP BY date, platform
ORDER BY date, platform;


-- ── 3. Top campaigns by conversion volume ────────────────────
SELECT
  platform,
  campaign_name,
  SUM(conversions)                                    AS total_conversions,
  ROUND(SUM(spend), 2)                                AS total_spend,
  ROUND(SAFE_DIVIDE(SUM(spend), SUM(conversions)), 2) AS cpa,
  ROUND(SAFE_DIVIDE(SUM(clicks), SUM(impressions)) * 100, 2) AS ctr_pct
FROM `marketing_analytics.unified_ads`
GROUP BY platform, campaign_name
ORDER BY total_conversions DESC;


-- ── 4. Week-over-week spend & conversion change ───────────────
WITH weekly AS (
  SELECT
    DATE_TRUNC(date, WEEK)  AS week_start,
    platform,
    SUM(spend)              AS spend,
    SUM(conversions)        AS conversions
  FROM `marketing_analytics.unified_ads`
  GROUP BY 1, 2
)
SELECT
  week_start,
  platform,
  ROUND(spend, 2)                             AS spend,
  conversions,
  ROUND(
    SAFE_DIVIDE(
      spend - LAG(spend) OVER (PARTITION BY platform ORDER BY week_start),
      LAG(spend) OVER (PARTITION BY platform ORDER BY week_start)
    ) * 100, 1
  )                                           AS spend_wow_pct,
  ROUND(
    SAFE_DIVIDE(
      conversions - LAG(conversions) OVER (PARTITION BY platform ORDER BY week_start),
      LAG(conversions) OVER (PARTITION BY platform ORDER BY week_start)
    ) * 100, 1
  )                                           AS conv_wow_pct
FROM weekly
ORDER BY week_start, platform;


-- ── 5. TikTok video completion funnel ────────────────────────
SELECT
  campaign_name,
  SUM(impressions)                                              AS impressions,
  SUM(video_views)                                             AS video_views,
  ROUND(SAFE_DIVIDE(SUM(video_views), SUM(impressions)) * 100, 1)  AS view_rate_pct,
  ROUND(AVG(video_watch_25_pct)  * 100, 1)                    AS avg_watch_25_pct,
  ROUND(AVG(video_watch_50_pct)  * 100, 1)                    AS avg_watch_50_pct,
  ROUND(AVG(video_watch_75_pct)  * 100, 1)                    AS avg_watch_75_pct,
  ROUND(AVG(video_watch_100_pct) * 100, 1)                    AS avg_watch_100_pct
FROM `marketing_analytics.unified_ads`
WHERE platform = 'TikTok'
GROUP BY campaign_name
ORDER BY view_rate_pct DESC;


-- ── 6. Data quality check ─────────────────────────────────────
SELECT
  platform,
  COUNT(*)                                            AS total_rows,
  COUNTIF(spend IS NULL OR spend < 0)                 AS bad_spend,
  COUNTIF(impressions IS NULL OR impressions < 0)     AS bad_impressions,
  COUNTIF(clicks > impressions)                       AS clicks_exceed_impressions,
  COUNTIF(conversions > clicks)                       AS conv_exceed_clicks,
  COUNTIF(ctr > 1)                                    AS ctr_above_100pct
FROM `marketing_analytics.unified_ads`
GROUP BY platform;
