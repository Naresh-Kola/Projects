import streamlit as st

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon=":material/shopping_cart:",
    layout="wide",
)

page = st.navigation(
    [
        st.Page("app_pages/revenue_overview.py", title="Revenue Overview", icon=":material/attach_money:"),
        st.Page("app_pages/customer_insights.py", title="Customer Insights", icon=":material/group:"),
        st.Page("app_pages/product_performance.py", title="Product Performance", icon=":material/inventory:"),
        st.Page("app_pages/customer_ltv.py", title="Customer LTV", icon=":material/trending_up:"),
    ],
    position="sidebar",
)

st.sidebar.caption("ECOM_ANALYTICS | ECOM_WH | ACCOUNTADMIN")

page.run()
