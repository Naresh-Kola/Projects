import streamlit as st
import altair as alt
import pandas as pd

# --- Custom CSS for card styling ---
st.markdown("""
<style>
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8f9fc 0%, #ffffff 100%);
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        padding: 12px 16px;
    }
    div[data-testid="stMetric"] label {
        font-size: 0.85rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 1.6rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

conn = st.connection("snowflake")

st.title(":material/attach_money: Revenue Overview")

# ── Data loading ──────────────────────────────────────────────
daily = conn.query("""
    SELECT REVENUE_DATE, TOTAL_ORDERS, DAILY_REVENUE
    FROM ECOM_ANALYTICS.METRICS.DAILY_REVENUE
    ORDER BY REVENUE_DATE
""", ttl=600)

products = conn.query("""
    SELECT PRODUCT_NAME, CATEGORY, TOTAL_REVENUE
    FROM ECOM_ANALYTICS.METRICS.PRODUCT_PERFORMANCE
    ORDER BY TOTAL_REVENUE DESC
""", ttl=600)

daily["REVENUE_DATE"] = pd.to_datetime(daily["REVENUE_DATE"])

# ── Monthly aggregation for KPI deltas ────────────────────────
monthly = (
    daily
    .assign(MONTH=daily["REVENUE_DATE"].dt.to_period("M"))
    .groupby("MONTH")
    .agg(MONTHLY_REV=("DAILY_REVENUE", "sum"),
         MONTHLY_ORD=("TOTAL_ORDERS", "sum"))
    .reset_index()
    .sort_values("MONTH")
)

# Use last two full months (skip current partial month)
full_months = monthly[monthly["MONTH"] < monthly["MONTH"].iloc[-1]]
if len(full_months) >= 2:
    curr_m = full_months.iloc[-1]
    prev_m = full_months.iloc[-2]
else:
    curr_m = monthly.iloc[-1]
    prev_m = monthly.iloc[-2] if len(monthly) >= 2 else curr_m

curr_rev = curr_m["MONTHLY_REV"]
prev_rev = prev_m["MONTHLY_REV"]
curr_ord = int(curr_m["MONTHLY_ORD"])
prev_ord = int(prev_m["MONTHLY_ORD"])
curr_aov = curr_rev / curr_ord if curr_ord else 0
prev_aov = prev_rev / prev_ord if prev_ord else 0
mom_growth = ((curr_rev - prev_rev) / prev_rev * 100) if prev_rev else 0

# ── KPI row ───────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(
        "Total Revenue",
        f"${daily['DAILY_REVENUE'].sum():,.0f}",
        delta=f"${curr_rev - prev_rev:+,.0f} vs prior month",
        border=True,
    )
with k2:
    st.metric(
        "Total Orders",
        f"{int(daily['TOTAL_ORDERS'].sum()):,}",
        delta=f"{curr_ord - prev_ord:+,} vs prior month",
        border=True,
    )
with k3:
    st.metric(
        "Avg Order Value",
        f"${curr_aov:,.2f}",
        delta=f"${curr_aov - prev_aov:+,.2f} vs prior month",
        border=True,
    )
with k4:
    st.metric(
        "MoM Revenue Growth",
        f"{mom_growth:+.1f}%",
        delta=f"{mom_growth:+.1f}% month-over-month",
        border=True,
    )

st.divider()

# ── Revenue trend area chart ──────────────────────────────────
with st.container(border=True):
    left_hdr, right_sel = st.columns([3, 1])
    with left_hdr:
        st.subheader("Revenue trend")
    with right_sel:
        granularity = st.selectbox(
            "Granularity",
            ["Daily", "Weekly", "Monthly"],
            index=0,
            label_visibility="collapsed",
        )

    # Resample based on selection
    ts = daily.set_index("REVENUE_DATE")
    if granularity == "Weekly":
        trend = (
            ts.resample("W")
            .agg({"DAILY_REVENUE": "sum", "TOTAL_ORDERS": "sum"})
            .reset_index()
        )
    elif granularity == "Monthly":
        trend = (
            ts.resample("ME")
            .agg({"DAILY_REVENUE": "sum", "TOTAL_ORDERS": "sum"})
            .reset_index()
        )
    else:
        trend = daily.copy()

    trend = trend.rename(columns={"REVENUE_DATE": "DATE", "DAILY_REVENUE": "REVENUE", "TOTAL_ORDERS": "ORDERS"})

    # Layered area + line chart
    base = alt.Chart(trend).encode(
        x=alt.X("DATE:T", title="Date"),
        tooltip=[
            alt.Tooltip("DATE:T", title="Date"),
            alt.Tooltip("REVENUE:Q", title="Revenue", format="$,.0f"),
            alt.Tooltip("ORDERS:Q", title="Orders", format=","),
        ],
    )

    area = base.mark_area(
        line={"color": "#4F46E5", "strokeWidth": 2},
        color=alt.Gradient(
            gradient="linear",
            stops=[
                alt.GradientStop(color="#4F46E5", offset=1),
                alt.GradientStop(color="rgba(79, 70, 229, 0.05)", offset=0),
            ],
            x1=1, x2=1, y1=1, y2=0,
        ),
        interpolate="monotone",
    ).encode(
        y=alt.Y("REVENUE:Q", title="Revenue ($)"),
    )

    points = base.mark_circle(size=30, color="#4F46E5").encode(
        y=alt.Y("REVENUE:Q"),
    )

    st.altair_chart(area + points, use_container_width=True)

# ── Bottom row: Category donut + Summary stats ───────────────
col_chart, col_stats = st.columns([2, 1])

with col_chart:
    with st.container(border=True):
        st.subheader("Revenue by category")

        cat_data = products.groupby("CATEGORY")["TOTAL_REVENUE"].sum().reset_index()
        cat_total = cat_data["TOTAL_REVENUE"].sum()
        cat_data["PCT"] = (cat_data["TOTAL_REVENUE"] / cat_total * 100).round(1)

        donut = (
            alt.Chart(cat_data)
            .mark_arc(innerRadius=65, outerRadius=120, cornerRadius=4)
            .encode(
                theta=alt.Theta("TOTAL_REVENUE:Q", stack=True),
                color=alt.Color(
                    "CATEGORY:N",
                    title="Category",
                    scale=alt.Scale(
                        domain=["Electronics", "Apparel", "Home & Kitchen", "Footwear"],
                        range=["#4F46E5", "#06B6D4", "#F59E0B", "#EF4444"],
                    ),
                ),
                tooltip=[
                    alt.Tooltip("CATEGORY:N", title="Category"),
                    alt.Tooltip("TOTAL_REVENUE:Q", title="Revenue", format="$,.0f"),
                    alt.Tooltip("PCT:Q", title="Share", format=".1f"),
                ],
            )
        )

        text_overlay = (
            alt.Chart(pd.DataFrame({"label": [f"${cat_total/1e6:.1f}M"], "x": [0], "y": [0]}))
            .mark_text(fontSize=18, fontWeight="bold", color="#374151")
            .encode(x=alt.value(150), y=alt.value(150), text="label:N")
        )

        st.altair_chart(donut + text_overlay, use_container_width=True)

with col_stats:
    with st.container(border=True):
        st.subheader("Summary")

        best_day = daily.loc[daily["DAILY_REVENUE"].idxmax()]
        best_month_data = full_months.loc[full_months["MONTHLY_REV"].idxmax()] if len(full_months) > 0 else monthly.iloc[-1]

        st.metric(
            "Best day",
            f"${best_day['DAILY_REVENUE']:,.0f}",
            delta=best_day["REVENUE_DATE"].strftime("%b %d, %Y"),
            delta_color="off",
            border=True,
        )
        st.metric(
            "Best month",
            f"${best_month_data['MONTHLY_REV']:,.0f}",
            delta=str(best_month_data["MONTH"]),
            delta_color="off",
            border=True,
        )
        st.metric(
            "Avg daily revenue",
            f"${daily['DAILY_REVENUE'].mean():,.0f}",
            border=True,
        )
        st.metric(
            "Categories",
            len(cat_data),
            border=True,
        )
