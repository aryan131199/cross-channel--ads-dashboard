import os
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, dash_table
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Load raw CSVs ──────────────────────────────────────────────────────────
fb   = pd.read_csv(os.path.join(BASE, "01_facebook_ads.csv"),  parse_dates=["date"])
goog = pd.read_csv(os.path.join(BASE, "02_google_ads.csv"),    parse_dates=["date"])
tt   = pd.read_csv(os.path.join(BASE, "03_tiktok_ads.csv"),    parse_dates=["date"])

# ── Build unified table (mirrors SQL 02_create_unified_table.sql) ──────────
fb_u = pd.DataFrame({
    "date": fb["date"], "platform": "Facebook",
    "campaign_id": fb["campaign_id"], "campaign_name": fb["campaign_name"],
    "ad_group_id": fb["ad_set_id"],  "ad_group_name": fb["ad_set_name"],
    "impressions": fb["impressions"], "clicks": fb["clicks"],
    "spend": fb["spend"],            "conversions": fb["conversions"],
    "video_views": fb["video_views"],"reach": fb["reach"],
    "engagement_rate": fb["engagement_rate"],
    "conversion_value": np.nan, "quality_score": np.nan,
    "likes": np.nan, "shares": np.nan, "comments": np.nan,
    "video_watch_25": np.nan, "video_watch_50": np.nan,
    "video_watch_75": np.nan, "video_watch_100": np.nan,
})

goog_u = pd.DataFrame({
    "date": goog["date"], "platform": "Google",
    "campaign_id": goog["campaign_id"], "campaign_name": goog["campaign_name"],
    "ad_group_id": goog["ad_group_id"], "ad_group_name": goog["ad_group_name"],
    "impressions": goog["impressions"], "clicks": goog["clicks"],
    "spend": goog["cost"],              "conversions": goog["conversions"],
    "video_views": np.nan, "reach": np.nan, "engagement_rate": np.nan,
    "conversion_value": goog["conversion_value"],
    "quality_score": goog["quality_score"],
    "likes": np.nan, "shares": np.nan, "comments": np.nan,
    "video_watch_25": np.nan, "video_watch_50": np.nan,
    "video_watch_75": np.nan, "video_watch_100": np.nan,
})

tt_u = pd.DataFrame({
    "date": tt["date"], "platform": "TikTok",
    "campaign_id": tt["campaign_id"], "campaign_name": tt["campaign_name"],
    "ad_group_id": tt["adgroup_id"],  "ad_group_name": tt["adgroup_name"],
    "impressions": tt["impressions"], "clicks": tt["clicks"],
    "spend": tt["cost"],              "conversions": tt["conversions"],
    "video_views": tt["video_views"], "reach": np.nan, "engagement_rate": np.nan,
    "conversion_value": np.nan, "quality_score": np.nan,
    "likes": tt["likes"], "shares": tt["shares"], "comments": tt["comments"],
    "video_watch_25": tt["video_watch_25"], "video_watch_50": tt["video_watch_50"],
    "video_watch_75": tt["video_watch_75"], "video_watch_100": tt["video_watch_100"],
})

df = pd.concat([fb_u, goog_u, tt_u], ignore_index=True)
df["ctr"]             = df["clicks"]      / df["impressions"]
df["cpc"]             = df["spend"]       / df["clicks"]
df["cpa"]             = df["spend"]       / df["conversions"]
df["conversion_rate"] = df["conversions"] / df["clicks"]

# ── Design tokens ──────────────────────────────────────────────────────────
C = {
    "bg":       "#0D1117",
    "surface":  "#161B22",
    "card":     "#1C2128",
    "border":   "#30363D",
    "text":     "#E6EDF3",
    "muted":    "#7D8590",
    "FB":       "#1877F2",
    "Google":   "#EA4335",
    "TikTok":   "#69C9D0",
    "green":    "#3FB950",
    "yellow":   "#D29922",
    "red":      "#F85149",
    "grid":     "#21262D",
}
PLATFORM_COLORS = {"Facebook": C["FB"], "Google": C["Google"], "TikTok": C["TikTok"]}
COLOR_SEQ       = [C["FB"], C["Google"], C["TikTok"]]

FONT = "Inter, -apple-system, BlinkMacSystemFont, sans-serif"

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family=FONT, color=C["text"], size=12),
    margin=dict(l=8, r=8, t=36, b=8),
    legend=dict(
        bgcolor="rgba(0,0,0,0)", bordercolor=C["border"],
        borderwidth=1, font=dict(size=11),
        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
    ),
    hoverlabel=dict(
        bgcolor=C["card"], bordercolor=C["border"],
        font=dict(family=FONT, size=12, color=C["text"]),
    ),
)

AXIS_STYLE = dict(gridcolor=C["grid"], linecolor=C["border"], tickfont=dict(size=11))

# ── Aggregations ───────────────────────────────────────────────────────────
total_spend       = df["spend"].sum()
total_impressions = df["impressions"].sum()
total_clicks      = df["clicks"].sum()
total_conversions = df["conversions"].sum()
overall_ctr       = total_clicks / total_impressions * 100
overall_cpa       = total_spend  / total_conversions
overall_cpc       = total_spend  / total_clicks

by_platform = (
    df.groupby("platform")
      .agg(spend=("spend","sum"), impressions=("impressions","sum"),
           clicks=("clicks","sum"), conversions=("conversions","sum"))
      .reset_index()
)
by_platform["ctr"] = by_platform["clicks"] / by_platform["impressions"] * 100
by_platform["cpa"] = by_platform["spend"]  / by_platform["conversions"]
by_platform["cpc"] = by_platform["spend"]  / by_platform["clicks"]

daily = (
    df.groupby(["date","platform"])
      .agg(spend=("spend","sum"), conversions=("conversions","sum"),
           clicks=("clicks","sum"), impressions=("impressions","sum"))
      .reset_index()
)

by_campaign = (
    df.groupby(["platform","campaign_name"])
      .agg(spend=("spend","sum"), impressions=("impressions","sum"),
           clicks=("clicks","sum"), conversions=("conversions","sum"))
      .reset_index()
)
by_campaign["ctr"] = (by_campaign["clicks"] / by_campaign["impressions"] * 100).round(2)
by_campaign["cpa"] = (by_campaign["spend"]  / by_campaign["conversions"]).round(2)
by_campaign["cpc"] = (by_campaign["spend"]  / by_campaign["clicks"]).round(2)

# TikTok video funnel (raw totals)
tt_campaigns = tt.groupby("campaign_name").agg(
    impressions=("impressions","sum"),
    video_views=("video_views","sum"),
    w25=("video_watch_25","sum"),
    w50=("video_watch_50","sum"),
    w75=("video_watch_75","sum"),
    w100=("video_watch_100","sum"),
    likes=("likes","sum"),
    shares=("shares","sum"),
    comments=("comments","sum"),
).reset_index()


# ══════════════════════════════════════════════════════════════════════════
# CHART BUILDERS
# ══════════════════════════════════════════════════════════════════════════

def kpi_card(label, value, sub=None, color=C["green"]):
    return html.Div([
        html.P(label, style={"margin":"0 0 4px","fontSize":"11px",
                              "textTransform":"uppercase","letterSpacing":"1px",
                              "color":C["muted"],"fontWeight":"600"}),
        html.H3(value, style={"margin":"0","fontSize":"26px","fontWeight":"700",
                               "color":C["text"],"lineHeight":"1"}),
        html.P(sub or "", style={"margin":"4px 0 0","fontSize":"11px","color":color}),
    ], style={
        "background":C["card"],"border":f"1px solid {C['border']}",
        "borderRadius":"10px","padding":"18px 22px","flex":"1",
        "borderTop":f"3px solid {color}",
    })


def fig_spend_donut():
    fig = go.Figure(go.Pie(
        labels=by_platform["platform"],
        values=by_platform["spend"].round(2),
        hole=0.62,
        marker=dict(colors=COLOR_SEQ, line=dict(color=C["bg"], width=3)),
        textinfo="label+percent",
        textfont=dict(size=12, color=C["text"]),
        hovertemplate="<b>%{label}</b><br>Spend: $%{value:,.0f}<br>Share: %{percent}<extra></extra>",
    ))
    total = f"${total_spend:,.0f}"
    fig.add_annotation(text=total, x=0.5, y=0.54, font=dict(size=18, color=C["text"], family=FONT),
                       showarrow=False)
    fig.add_annotation(text="Total Spend", x=0.5, y=0.44, font=dict(size=11, color=C["muted"], family=FONT),
                       showarrow=False)
    fig.update_layout(**CHART_LAYOUT, title=dict(text="Spend Share by Platform",
                      font=dict(size=13, color=C["muted"]), x=0, xref="paper"),
                      showlegend=False, height=300)
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig


FILL_COLORS = {
    "Facebook": "rgba(24,119,242,0.08)",
    "Google":   "rgba(234,67,53,0.08)",
    "TikTok":   "rgba(105,201,208,0.08)",
}

def fig_spend_trend():
    fig = go.Figure()
    for plat, color in PLATFORM_COLORS.items():
        d = daily[daily["platform"] == plat].sort_values("date")
        fig.add_trace(go.Scatter(
            x=d["date"], y=d["spend"].round(2),
            name=plat, mode="lines",
            line=dict(color=color, width=2.5),
            fill="tozeroy", fillcolor=FILL_COLORS[plat],
            hovertemplate=f"<b>{plat}</b><br>%{{x|%b %d}}<br>${{y:,.0f}}<extra></extra>",
        ))
    fig.update_layout(**CHART_LAYOUT, title=dict(text="Daily Spend by Platform",
                      font=dict(size=13, color=C["muted"]), x=0, xref="paper"),
                      height=300, hovermode="x unified")
    fig.update_xaxes(**AXIS_STYLE, showgrid=False)
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def fig_ctr_bar():
    bp = by_platform.sort_values("ctr")
    colors = [PLATFORM_COLORS[p] for p in bp["platform"]]
    fig = go.Figure(go.Bar(
        x=bp["ctr"].round(3),
        y=bp["platform"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v:.2f}%" for v in bp["ctr"]],
        textposition="outside",
        textfont=dict(size=12, color=C["text"]),
        hovertemplate="<b>%{y}</b><br>CTR: %{x:.3f}%<extra></extra>",
        width=0.5,
    ))
    fig.update_layout(**CHART_LAYOUT, title=dict(text="Click-Through Rate by Platform",
                      font=dict(size=13, color=C["muted"]), x=0, xref="paper"),
                      height=240, xaxis_title="CTR (%)")
    fig.update_xaxes(**AXIS_STYLE, ticksuffix="%")
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def fig_cpa_bar():
    bp = by_platform.sort_values("cpa", ascending=False)
    colors = [PLATFORM_COLORS[p] for p in bp["platform"]]
    fig = go.Figure(go.Bar(
        x=bp["cpa"].round(2),
        y=bp["platform"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"${v:.2f}" for v in bp["cpa"]],
        textposition="outside",
        textfont=dict(size=12, color=C["text"]),
        hovertemplate="<b>%{y}</b><br>CPA: $%{x:.2f}<extra></extra>",
        width=0.5,
    ))
    fig.update_layout(**CHART_LAYOUT, title=dict(text="Cost per Acquisition by Platform",
                      font=dict(size=13, color=C["muted"]), x=0, xref="paper"),
                      height=240, xaxis_title="CPA ($)")
    fig.update_xaxes(**AXIS_STYLE, tickprefix="$")
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def fig_conversions_trend():
    fig = go.Figure()
    for plat, color in PLATFORM_COLORS.items():
        d = daily[daily["platform"] == plat].sort_values("date")
        fig.add_trace(go.Bar(
            x=d["date"], y=d["conversions"],
            name=plat, marker_color=color,
            hovertemplate=f"<b>{plat}</b><br>%{{x|%b %d}}<br>%{{y:,}} conversions<extra></extra>",
        ))
    fig.update_layout(**CHART_LAYOUT, title=dict(text="Daily Conversions by Platform",
                      font=dict(size=13, color=C["muted"]), x=0, xref="paper"),
                      barmode="stack", height=300, hovermode="x unified")
    fig.update_xaxes(**AXIS_STYLE, showgrid=False)
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def fig_efficiency_scatter():
    bc = by_campaign.copy()
    bc["color"] = bc["platform"].map(PLATFORM_COLORS)
    fig = go.Figure()
    for plat, color in PLATFORM_COLORS.items():
        d = bc[bc["platform"] == plat]
        fig.add_trace(go.Scatter(
            x=d["spend"], y=d["conversions"],
            mode="markers+text",
            name=plat,
            marker=dict(color=color, size=d["ctr"] * 500, opacity=0.75,
                        line=dict(color=C["border"], width=1)),
            text=d["campaign_name"].str.replace("_", " "),
            textposition="top center",
            textfont=dict(size=9, color=C["muted"]),
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Spend: $%{x:,.0f}<br>"
                "Conversions: %{y:,}<br>"
                "<extra></extra>"
            ),
        ))
    fig.update_layout(**CHART_LAYOUT,
                      title=dict(text="Spend vs. Conversions by Campaign (bubble size = CTR)",
                                 font=dict(size=13, color=C["muted"]), x=0, xref="paper"),
                      height=360, xaxis_title="Total Spend ($)", yaxis_title="Total Conversions")
    fig.update_xaxes(**AXIS_STYLE, tickprefix="$")
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def fig_tiktok_funnel():
    totals = tt_campaigns[["impressions","video_views","w25","w50","w75","w100"]].sum()
    stages = ["Impressions","Video Views","25% Watched","50% Watched","75% Watched","100% Watched"]
    values = [
        int(totals["impressions"]),
        int(totals["video_views"]),
        int(totals["w25"]),
        int(totals["w50"]),
        int(totals["w75"]),
        int(totals["w100"]),
    ]
    pcts = [100] + [round(v / values[0] * 100, 1) for v in values[1:]]
    fig = go.Figure(go.Funnel(
        y=stages, x=values,
        textposition="inside",
        text=[f"{p}%" for p in pcts],
        textfont=dict(color=C["text"], size=12),
        marker=dict(
            color=[C["TikTok"], "#56B8BF", "#3FA5AC", "#2E909A", "#1D7B87", "#0E6673"],
            line=dict(color=C["bg"], width=2),
        ),
        connector=dict(line=dict(color=C["border"], width=1)),
        hovertemplate="<b>%{y}</b><br>Count: %{x:,}<br>%{text} of impressions<extra></extra>",
    ))
    layout = {**CHART_LAYOUT, "margin": dict(l=140, r=8, t=36, b=8)}
    fig.update_layout(**layout,
                      title=dict(text="TikTok Video Completion Funnel",
                                 font=dict(size=13, color=C["muted"]), x=0, xref="paper"),
                      height=340)
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def fig_tiktok_engagement():
    tc = tt_campaigns.copy()
    tc["engagement_total"] = tc["likes"] + tc["shares"] + tc["comments"]
    tc = tc.sort_values("engagement_total", ascending=True)

    fig = go.Figure()
    for metric, color in [("likes", C["FB"]), ("shares", C["green"]), ("comments", C["yellow"])]:
        fig.add_trace(go.Bar(
            x=tc[metric], y=tc["campaign_name"].str.replace("_", " "),
            orientation="h", name=metric.capitalize(),
            marker=dict(color=color, line=dict(width=0)),
            hovertemplate=f"<b>%{{y}}</b><br>{metric.capitalize()}: %{{x:,}}<extra></extra>",
        ))
    fig.update_layout(**CHART_LAYOUT, barmode="stack",
                      title=dict(text="TikTok Engagement by Campaign",
                                 font=dict(size=13, color=C["muted"]), x=0, xref="paper"),
                      height=260)
    fig.update_xaxes(**AXIS_STYLE, showgrid=True)
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def build_campaign_table():
    tbl = by_campaign.copy()
    tbl["Spend"]       = tbl["spend"].apply(lambda x: f"${x:,.0f}")
    tbl["Impressions"] = tbl["impressions"].apply(lambda x: f"{x:,}")
    tbl["Clicks"]      = tbl["clicks"].apply(lambda x: f"{x:,}")
    tbl["Conversions"] = tbl["conversions"].apply(lambda x: f"{x:,}")
    tbl["CTR"]         = tbl["ctr"].apply(lambda x: f"{x:.2f}%")
    tbl["CPC"]         = tbl["cpc"].apply(lambda x: f"${x:.2f}")
    tbl["CPA"]         = tbl["cpa"].apply(lambda x: f"${x:.2f}")
    tbl = tbl.sort_values("conversions", ascending=False)
    tbl["Campaign"] = tbl["campaign_name"].str.replace("_", " ")
    tbl["Platform"] = tbl["platform"]

    display = tbl[["Platform","Campaign","Spend","Impressions","Clicks",
                   "Conversions","CTR","CPC","CPA"]]

    return dash_table.DataTable(
        data=display.to_dict("records"),
        columns=[{"name": c, "id": c} for c in display.columns],
        sort_action="native",
        style_table={"overflowX": "auto", "borderRadius": "8px"},
        style_header={
            "backgroundColor": C["surface"], "color": C["muted"],
            "fontWeight": "600", "fontSize": "11px", "textTransform": "uppercase",
            "letterSpacing": "0.8px", "border": f"1px solid {C['border']}",
            "padding": "10px 14px",
        },
        style_cell={
            "backgroundColor": C["card"], "color": C["text"],
            "border": f"1px solid {C['border']}", "fontFamily": FONT,
            "fontSize": "12px", "padding": "10px 14px",
            "textAlign": "left",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"},  "backgroundColor": C["surface"]},
            {"if": {"filter_query": '{Platform} = "Facebook"', "column_id": "Platform"},
             "color": C["FB"], "fontWeight": "600"},
            {"if": {"filter_query": '{Platform} = "Google"',   "column_id": "Platform"},
             "color": C["Google"], "fontWeight": "600"},
            {"if": {"filter_query": '{Platform} = "TikTok"',   "column_id": "Platform"},
             "color": C["TikTok"], "fontWeight": "600"},
        ],
        page_size=12,
    )


# ══════════════════════════════════════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════════════════════════════════════

def section_title(text):
    return html.H4(text, style={
        "color": C["muted"], "fontSize": "11px", "fontWeight": "700",
        "textTransform": "uppercase", "letterSpacing": "1.2px",
        "margin": "28px 0 12px", "borderBottom": f"1px solid {C['border']}",
        "paddingBottom": "8px",
    })


def chart_card(children, style=None):
    base = {
        "background": C["card"], "border": f"1px solid {C['border']}",
        "borderRadius": "10px", "padding": "16px",
    }
    if style:
        base.update(style)
    return html.Div(children, style=base)


app = dash.Dash(__name__, title="Improvado – Cross-Channel Ads Dashboard")
server = app.server  # exposed for gunicorn / Render deployment

app.layout = html.Div(style={
    "background": C["bg"], "minHeight": "100vh",
    "fontFamily": FONT, "color": C["text"],
}, children=[

    # ── Header ────────────────────────────────────────────────────────────
    html.Div([
        html.Div([
            html.H1("Cross-Channel Ads Performance",
                    style={"margin":"0","fontSize":"20px","fontWeight":"700","color":C["text"]}),
            html.P("Facebook · Google · TikTok  |  Jan 2024  |  Unified View",
                   style={"margin":"4px 0 0","fontSize":"12px","color":C["muted"]}),
        ]),
        html.Div([
            html.Span("● Live", style={"color": C["green"], "fontSize": "12px",
                                        "fontWeight": "600", "marginRight": "8px"}),
            html.Span("30-day window", style={"color": C["muted"], "fontSize": "12px"}),
        ]),
    ], style={
        "background": C["surface"], "border": f"1px solid {C['border']}",
        "borderRadius": "0 0 12px 12px", "padding": "18px 32px",
        "display": "flex", "justifyContent": "space-between", "alignItems": "center",
        "marginBottom": "24px",
    }),

    html.Div(style={"maxWidth": "1400px", "margin": "0 auto", "padding": "0 24px 48px"}, children=[

        # ── KPI Row ───────────────────────────────────────────────────────
        section_title("Key Performance Indicators"),
        html.Div([
            kpi_card("Total Spend",       f"${total_spend:,.0f}",
                     f"${by_platform.set_index('platform')['spend']['Facebook']:,.0f} FB · "
                     f"${by_platform.set_index('platform')['spend']['Google']:,.0f} G · "
                     f"${by_platform.set_index('platform')['spend']['TikTok']:,.0f} TT",
                     C["FB"]),
            kpi_card("Total Impressions", f"{total_impressions/1e6:.1f}M",
                     "All platforms combined", C["Google"]),
            kpi_card("Total Clicks",      f"{total_clicks:,.0f}",
                     f"Overall CTR: {overall_ctr:.2f}%", C["TikTok"]),
            kpi_card("Total Conversions", f"{int(total_conversions):,}",
                     "Across all campaigns", C["green"]),
            kpi_card("Avg CPA",           f"${overall_cpa:.2f}",
                     "Cost per acquisition", C["yellow"]),
            kpi_card("Avg CPC",           f"${overall_cpc:.2f}",
                     "Cost per click", C["red"]),
        ], style={"display":"flex","gap":"12px","flexWrap":"wrap"}),

        # ── Spend Overview ────────────────────────────────────────────────
        section_title("Spend Overview"),
        html.Div([
            chart_card(dcc.Graph(figure=fig_spend_donut(), config={"displayModeBar":False}),
                       {"flex":"0 0 300px"}),
            chart_card(dcc.Graph(figure=fig_spend_trend(), config={"displayModeBar":False}),
                       {"flex":"1"}),
        ], style={"display":"flex","gap":"12px"}),

        # ── Efficiency Metrics ────────────────────────────────────────────
        section_title("Platform Efficiency"),
        html.Div([
            chart_card(dcc.Graph(figure=fig_ctr_bar(), config={"displayModeBar":False}),
                       {"flex":"1"}),
            chart_card(dcc.Graph(figure=fig_cpa_bar(), config={"displayModeBar":False}),
                       {"flex":"1"}),
        ], style={"display":"flex","gap":"12px"}),

        # ── Conversions + Scatter ─────────────────────────────────────────
        section_title("Conversion Performance"),
        html.Div([
            chart_card(dcc.Graph(figure=fig_conversions_trend(), config={"displayModeBar":False}),
                       {"flex":"1"}),
            chart_card(dcc.Graph(figure=fig_efficiency_scatter(), config={"displayModeBar":False}),
                       {"flex":"1"}),
        ], style={"display":"flex","gap":"12px"}),

        # ── TikTok Deep Dive ──────────────────────────────────────────────
        section_title("TikTok – Video & Engagement Insights"),
        html.Div([
            chart_card(dcc.Graph(figure=fig_tiktok_funnel(), config={"displayModeBar":False}),
                       {"flex":"1"}),
            chart_card(dcc.Graph(figure=fig_tiktok_engagement(), config={"displayModeBar":False}),
                       {"flex":"1"}),
        ], style={"display":"flex","gap":"12px"}),

        # ── Campaign Table ────────────────────────────────────────────────
        section_title("Campaign Performance Table"),
        chart_card(build_campaign_table()),

        # ── Footer ────────────────────────────────────────────────────────
        html.P("Data: Facebook Ads · Google Ads · TikTok Ads  |  Period: Jan 1–30 2024  |  "
               "Built with Plotly Dash",
               style={"textAlign":"center","color":C["muted"],"fontSize":"11px",
                      "marginTop":"32px","paddingTop":"16px",
                      "borderTop":f"1px solid {C['border']}"}),
    ]),
])

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
