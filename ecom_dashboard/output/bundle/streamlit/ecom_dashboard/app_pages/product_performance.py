import streamlit as st
import altair as alt

conn = st.connection("snowflake")

st.title(":material/inventory: Product Performance")

# --- Load product data ---
products = conn.query("""
    SELECT PRODUCT_ID, PRODUCT_NAME, CATEGORY,
           TOTAL_UNITS_SOLD, TOTAL_REVENUE, REVENUE_RANK
    FROM ECOM_ANALYTICS.METRICS.PRODUCT_PERFORMANCE
    ORDER BY REVENUE_RANK
""", ttl=600)

# --- KPI row ---
total_products = len(products)
total_units = int(products["TOTAL_UNITS_SOLD"].sum())
total_revenue = products["TOTAL_REVENUE"].sum()
top_product = products.iloc[0]["PRODUCT_NAME"]

with st.container(horizontal=True):
    st.metric("Products", total_products, border=True)
    st.metric("Total Units Sold", f"{total_units:,}", border=True)
    st.metric("Product Revenue", f"${total_revenue:,.2f}", border=True)
    st.metric("Top Product", top_product, border=True)

# --- Revenue by product bar chart ---
with st.container(border=True):
    st.subheader("Revenue by Product")
    chart = (
        alt.Chart(products)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("PRODUCT_NAME:N", title="Product", sort="-y"),
            y=alt.Y("TOTAL_REVENUE:Q", title="Revenue ($)"),
            color=alt.Color("CATEGORY:N", title="Category"),
            tooltip=[
                alt.Tooltip("PRODUCT_NAME:N", title="Product"),
                alt.Tooltip("CATEGORY:N", title="Category"),
                alt.Tooltip("TOTAL_REVENUE:Q", title="Revenue", format="$,.2f"),
                alt.Tooltip("TOTAL_UNITS_SOLD:Q", title="Units Sold"),
                alt.Tooltip("REVENUE_RANK:Q", title="Rank"),
            ],
        )
    )
    st.altair_chart(chart)

# --- Units sold + Category breakdown ---
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Units Sold by Product")
        chart = (
            alt.Chart(products)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("PRODUCT_NAME:N", title="Product", sort="-y"),
                y=alt.Y("TOTAL_UNITS_SOLD:Q", title="Units Sold"),
                tooltip=[
                    alt.Tooltip("PRODUCT_NAME:N", title="Product"),
                    alt.Tooltip("TOTAL_UNITS_SOLD:Q", title="Units Sold"),
                ],
            )
        )
        st.altair_chart(chart)

with col2:
    with st.container(border=True):
        st.subheader("Revenue by Category")
        cat_data = products.groupby("CATEGORY")["TOTAL_REVENUE"].sum().reset_index()
        chart = (
            alt.Chart(cat_data)
            .mark_arc(innerRadius=50)
            .encode(
                theta=alt.Theta("TOTAL_REVENUE:Q"),
                color=alt.Color("CATEGORY:N", title="Category"),
                tooltip=[
                    alt.Tooltip("CATEGORY:N", title="Category"),
                    alt.Tooltip("TOTAL_REVENUE:Q", title="Revenue", format="$,.2f"),
                ],
            )
        )
        st.altair_chart(chart)

# --- Product details table ---
with st.container(border=True):
    st.subheader("Product Rankings")
    st.dataframe(
        products,
        column_config={
            "PRODUCT_ID": st.column_config.NumberColumn("ID"),
            "PRODUCT_NAME": st.column_config.TextColumn("Product"),
            "CATEGORY": st.column_config.TextColumn("Category"),
            "TOTAL_UNITS_SOLD": st.column_config.NumberColumn("Units Sold"),
            "TOTAL_REVENUE": st.column_config.NumberColumn("Revenue", format="$%.2f"),
            "REVENUE_RANK": st.column_config.NumberColumn("Rank"),
        },
        hide_index=True,
    )
