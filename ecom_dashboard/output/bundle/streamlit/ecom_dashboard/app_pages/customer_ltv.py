import streamlit as st
import altair as alt

conn = st.connection("snowflake")

st.title(":material/trending_up: Customer LTV")

# --- Load LTV data ---
ltv = conn.query("""
    SELECT CUSTOMER_ID, FULL_NAME, EMAIL, COUNTRY, CUSTOMER_TIER,
           TOTAL_ORDERS, TOTAL_SPENT, TENURE_DAYS, PROJECTED_ANNUAL_VALUE
    FROM ECOM_ANALYTICS.METRICS.CUSTOMER_LTV
    ORDER BY PROJECTED_ANNUAL_VALUE DESC
""", ttl=600)

# --- KPI row ---
avg_ltv = ltv["PROJECTED_ANNUAL_VALUE"].mean()
max_ltv = ltv["PROJECTED_ANNUAL_VALUE"].max()
total_projected = ltv["PROJECTED_ANNUAL_VALUE"].sum()
top_customer = ltv.iloc[0]["FULL_NAME"]

with st.container(horizontal=True):
    st.metric("Avg Annual LTV", f"${avg_ltv:,.2f}", border=True)
    st.metric("Highest LTV", f"${max_ltv:,.2f}", border=True)
    st.metric("Total Projected Annual", f"${total_projected:,.2f}", border=True)
    st.metric("Top Customer", top_customer, border=True)

# --- LTV by customer bar chart ---
with st.container(border=True):
    st.subheader("Projected Annual Value by Customer")
    chart = (
        alt.Chart(ltv)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("FULL_NAME:N", title="Customer", sort="-y"),
            y=alt.Y("PROJECTED_ANNUAL_VALUE:Q", title="Projected Annual Value ($)"),
            color=alt.Color(
                "CUSTOMER_TIER:N",
                title="Tier",
                scale=alt.Scale(
                    domain=["Gold", "Silver", "Bronze"],
                    range=["#FFD700", "#C0C0C0", "#CD7F32"],
                ),
            ),
            tooltip=[
                alt.Tooltip("FULL_NAME:N", title="Customer"),
                alt.Tooltip("CUSTOMER_TIER:N", title="Tier"),
                alt.Tooltip("PROJECTED_ANNUAL_VALUE:Q", title="Projected Annual Value", format="$,.2f"),
                alt.Tooltip("TOTAL_SPENT:Q", title="Total Spent", format="$,.2f"),
                alt.Tooltip("TENURE_DAYS:Q", title="Tenure (days)"),
            ],
        )
    )
    st.altair_chart(chart)

# --- Spend vs LTV scatter ---
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Total Spent vs Projected LTV")
        chart = (
            alt.Chart(ltv)
            .mark_circle(size=100)
            .encode(
                x=alt.X("TOTAL_SPENT:Q", title="Total Spent ($)"),
                y=alt.Y("PROJECTED_ANNUAL_VALUE:Q", title="Projected Annual Value ($)"),
                color=alt.Color(
                    "CUSTOMER_TIER:N",
                    title="Tier",
                    scale=alt.Scale(
                        domain=["Gold", "Silver", "Bronze"],
                        range=["#FFD700", "#C0C0C0", "#CD7F32"],
                    ),
                ),
                tooltip=[
                    alt.Tooltip("FULL_NAME:N", title="Customer"),
                    alt.Tooltip("TOTAL_SPENT:Q", title="Total Spent", format="$,.2f"),
                    alt.Tooltip("PROJECTED_ANNUAL_VALUE:Q", title="LTV", format="$,.2f"),
                ],
            )
        )
        st.altair_chart(chart)

with col2:
    with st.container(border=True):
        st.subheader("LTV by Country")
        country_ltv = ltv.groupby("COUNTRY")["PROJECTED_ANNUAL_VALUE"].mean().reset_index()
        country_ltv.columns = ["COUNTRY", "AVG_LTV"]
        chart = (
            alt.Chart(country_ltv)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("COUNTRY:N", title="Country", sort="-y"),
                y=alt.Y("AVG_LTV:Q", title="Avg Projected LTV ($)"),
                tooltip=[
                    alt.Tooltip("COUNTRY:N", title="Country"),
                    alt.Tooltip("AVG_LTV:Q", title="Avg LTV", format="$,.2f"),
                ],
            )
        )
        st.altair_chart(chart)

# --- LTV details table ---
with st.container(border=True):
    st.subheader("Customer LTV Details")
    st.dataframe(
        ltv,
        column_config={
            "CUSTOMER_ID": st.column_config.NumberColumn("ID"),
            "FULL_NAME": st.column_config.TextColumn("Name"),
            "EMAIL": st.column_config.TextColumn("Email"),
            "COUNTRY": st.column_config.TextColumn("Country"),
            "CUSTOMER_TIER": st.column_config.TextColumn("Tier"),
            "TOTAL_ORDERS": st.column_config.NumberColumn("Orders"),
            "TOTAL_SPENT": st.column_config.NumberColumn("Total Spent", format="$%.2f"),
            "TENURE_DAYS": st.column_config.NumberColumn("Tenure (days)"),
            "PROJECTED_ANNUAL_VALUE": st.column_config.NumberColumn("Projected Annual Value", format="$%.2f"),
        },
        hide_index=True,
    )
