# Cross-Channel Ads Performance Dashboard
### Improvado – Marketing Analyst Technical Assignment

A production-ready, single-page analytics dashboard that unifies Facebook Ads, Google Ads, and TikTok Ads data into a cross-platform performance view. Built with Python, Plotly Dash, and pandas.

---

## What This Project Does

- Ingests 3 raw CSV files (Facebook, Google, TikTok) and builds a unified data model in-memory (mirroring the SQL schema in `/sql`)
- Renders a dark-themed, interactive dashboard with 10+ charts covering spend, CTR, CPA, conversions, video completion funnel, engagement, and a sortable campaign table
- Fully deployable as a live URL (Vercel or Render)

---

## Project Structure

```
marketing-analyst-assignment/
│
├── 01_facebook_ads.csv          # Raw Facebook Ads data (Jan 2024)
├── 02_google_ads.csv            # Raw Google Ads data (Jan 2024)
├── 03_tiktok_ads.csv            # Raw TikTok Ads data (Jan 2024)
│
├── dashboard/
│   └── app.py                   # Main Dash application (all charts + layout)
│
├── sql/
│   ├── 01_create_source_tables.sql   # BigQuery DDL for 3 source tables
│   ├── 02_create_unified_table.sql   # Unified cross-channel view / table
│   └── 03_analysis_queries.sql       # Analysis queries (KPIs, platform breakdown)
│
├── api/
│   └── index.py                 # Vercel WSGI entry point
│
├── requirements.txt             # Python dependencies
├── vercel.json                  # Vercel deployment config
├── render.yaml                  # Render.com deployment config (alternative)
└── README.md
```

---

## Dashboard Sections

| Section | Charts |
|---|---|
| Key Performance Indicators | 6 KPI cards: Spend, Impressions, Clicks, Conversions, CPA, CPC |
| Spend Overview | Donut (spend share) + Line trend (daily spend by platform) |
| Platform Efficiency | CTR bar chart + CPA bar chart |
| Conversion Performance | Stacked daily conversions + Spend vs Conversions scatter (bubble = CTR) |
| TikTok Deep Dive | Video completion funnel + Engagement by campaign (likes/shares/comments) |
| Campaign Table | Sortable table with all 12 campaigns across platforms |

---

## Local Setup

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

**2. Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the dashboard**
```bash
python dashboard/app.py
```

**5. Open in browser**
```
http://localhost:8050
```

The CSV files are read automatically from the project root — no database setup needed for local development.

---

## SQL Setup (BigQuery)

The `/sql` folder contains scripts to replicate the data model in BigQuery.

**Step 1** — Create a BigQuery dataset named `marketing_analytics`

**Step 2** — Upload the 3 CSVs as tables:
- `01_facebook_ads.csv` → `marketing_analytics.facebook_ads`
- `02_google_ads.csv` → `marketing_analytics.google_ads`
- `03_tiktok_ads.csv` → `marketing_analytics.tiktok_ads`

**Step 3** — Run SQL scripts in order:
```
sql/01_create_source_tables.sql   → creates the 3 typed source tables
sql/02_create_unified_table.sql   → creates the unified cross-channel table
sql/03_analysis_queries.sql       → optional analysis queries
```

---

## Deploy to Vercel (via GitHub)

> **Note:** Vercel works best for this app on the Hobby plan. If deployment fails due to bundle size, use [Render](#deploy-to-render-alternative) instead (already configured).

**Step 1 – Push to GitHub**
```bash
git init                        # if not already a git repo
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

**Step 2 – Connect to Vercel**
1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click **Add New → Project**
3. Select your repository from the list
4. Click **Import**

**Step 3 – Configure build settings**
- Framework Preset: **Other**
- Root Directory: `.` (leave as default)
- Build Command: leave empty
- Output Directory: leave empty
- Click **Deploy**

**Step 4 – Get your live URL**

Vercel will build and deploy. Your live URL will be:
```
https://your-repo-name.vercel.app
```

---

## Deploy to Render (Alternative)

The `render.yaml` is already configured. Render is more reliable for Python/WSGI apps.

**Step 1** – Push to GitHub (same as Vercel Step 1 above)

**Step 2** – Go to [render.com](https://render.com) → **New → Web Service**

**Step 3** – Connect your GitHub repo → Render reads `render.yaml` automatically

**Step 4** – Click **Create Web Service** → your URL will be:
```
https://improvado-ads-dashboard.onrender.com
```

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| dash | 2.17.1 | Web framework for the dashboard |
| plotly | 5.22.0 | Charts and visualizations |
| pandas | 2.2.2 | Data loading and transformation |
| numpy | 1.26.4 | Numeric operations |
| gunicorn | 22.0.0 | Production WSGI server (Render/Linux) |

---

## Data Period

All data covers **January 1–30, 2024** across 3 platforms and 12 campaigns.

| Platform | Campaigns | Total Spend |
|---|---|---|
| TikTok | 4 | ~$74,267 (57%) |
| Google | 4 | ~$37,686 (29%) |
| Facebook | 4 | ~$18,292 (14%) |
| **Total** | **12** | **$130,245** |
