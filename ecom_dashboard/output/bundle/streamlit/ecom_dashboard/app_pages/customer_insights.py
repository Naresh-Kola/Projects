import streamlit as st
import altair as alt

conn = st.connection("snowflake")

st.title(":material/group: Customer Insights")

# --- Load customer data ---
customers = conn.query("""
    SELECT CUSTOMER_ID, FULL_NAME, COUNTRY, CUSTOMER_TIER,
           TOTAL_ORDERS, TOTAL_SPENT
    FROM ECOM_ANALYTICS.MARTS.DIM_CUSTOMERS
    ORDER BY TOTAL_SPENT DESC
""", ttl=600)

# --- KPI card ---
st.metric("Total Customers", len(customers), border=True)

# --- Tier pie chart + Top customers bar chart ---
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Customer tier distribution")
        tier_data = customers.groupby("CUSTOMER_TIER").size().reset_index(name="COUNT")
        chart = (
            alt.Chart(tier_data)
            .mark_arc()
            .encode(
                theta=alt.Theta("COUNT:Q"),
                color=alt.Color(
                    "CUSTOMER_TIER:N",
                    title="Tier",
                    scale=alt.Scale(
                        domain=["Gold", "Silver", "Bronze"],
                        range=["#FFD700", "#C0C0C0", "#CD7F32"],
                    ),
                ),
                tooltip=[
                    alt.Tooltip("CUSTOMER_TIER:N", title="Tier"),
                    alt.Tooltip("COUNT:Q", title="Customers"),
                ],
            )
        )
        st.altair_chart(chart)

with col2:
    with st.container(border=True):
        st.subheader("Top customers by total spent")
        chart = (
            alt.Chart(customers)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("FULL_NAME:N", title="Customer", sort="-y"),
                y=alt.Y("TOTAL_SPENT:Q", title="Total Spent ($)"),
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
                    alt.Tooltip("TOTAL_SPENT:Q", title="Total Spent", format="$,.2f"),
                    alt.Tooltip("TOTAL_ORDERS:Q", title="Orders"),
                ],
            )
        )
        st.altair_chart(chart)
