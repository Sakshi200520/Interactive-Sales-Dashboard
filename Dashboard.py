"""
Final Streamlit Sales Dashboard (Compact Version)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker   # ✅ added

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Branding
st.markdown("## 🏢 Company Sales Dashboard")
st.markdown("### _Powered by Data Analytics_")

PALETTE = {
    "Laptop": "#378ADD",
    "Phone": "#1D9E75",
    "Tablet": "#BA7517",
    "Monitor": "#D4537E",
    "Headphones": "#7F77DD",
}

BASE_DIR = r"C:\Users\hp\Interactive Sales Dashboard"
DATA_PATH = BASE_DIR + r"\sales_data (3).csv"

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    return df

df = load_data()

# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
st.sidebar.header("Filters")

products = st.sidebar.multiselect(
    "Select Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Product"].isin(products)) &
    (df["Region"].isin(regions))
]

# ─────────────────────────────────────────────
# KPI SECTION
# ─────────────────────────────────────────────
st.title("📊 Sales Dashboard")

col1, col2, col3 = st.columns(3)

total_sales = filtered_df["Total_Sales"].sum()
total_orders = len(filtered_df)
avg_order = total_sales / total_orders if total_orders > 0 else 0

col1.metric("💰 Total Revenue", f"₹{total_sales:,.0f}")
col2.metric("📦 Orders", total_orders)
col3.metric("🧾 Avg Order Value", f"₹{avg_order:,.0f}")

# ─────────────────────────────────────────────
# MAIN CHARTS (2×2 GRID)
# ─────────────────────────────────────────────
st.subheader("📊 Key Visualizations")

daily = filtered_df.groupby("Date")["Total_Sales"].sum().reset_index()
prod = filtered_df.groupby("Product")["Total_Sales"].sum().reset_index()
region = filtered_df.groupby("Region")["Total_Sales"].sum().reset_index()

fig1 = px.line(daily, x="Date", y="Total_Sales", title="Daily Revenue Trend")
fig1.update_layout(template="plotly_white")

fig2 = px.bar(prod, x="Product", y="Total_Sales",
              color="Product", color_discrete_map=PALETTE,
              title="Revenue by Product")

fig3 = px.pie(region, names="Region", values="Total_Sales",
              title="Revenue by Region")

fig4 = px.scatter(
    filtered_df,
    x="Quantity",
    y="Price",
    size="Total_Sales",
    color="Product",
    color_discrete_map=PALETTE,
    title="Quantity vs Price"
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)

# ─────────────────────────────────────────────
# STATISTICAL ANALYSIS (FIXED)
# ─────────────────────────────────────────────
st.subheader("📊 Statistical Analysis")

colA, colB = st.columns(2)

with colA:
    fig_hist, ax = plt.subplots(figsize=(6, 3.5))
    sns.histplot(filtered_df["Total_Sales"], kde=True, ax=ax)

    ax.set_title("Sales Distribution", fontsize=10)

    # 🔥 FIX: clean x-axis numbers
    ax.xaxis.set_major_locator(ticker.MaxNLocator(5))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x/1000)}K'))

    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)

    plt.tight_layout()

    st.pyplot(fig_hist, use_container_width=False)

with colB:
    fig_box = px.box(filtered_df, x="Product", y="Total_Sales",
                     color="Product", color_discrete_map=PALETTE,
                     title="Sales Spread")
    st.plotly_chart(fig_box, use_container_width=True)

fig_violin = px.violin(filtered_df, x="Product", y="Total_Sales",
                       color="Product", box=True,
                       title="Distribution Shape")

fig_violin.update_layout(margin=dict(l=10, r=10, t=40, b=10))

st.plotly_chart(fig_violin, use_container_width=True)

# ─────────────────────────────────────────────
# HEATMAP
# ─────────────────────────────────────────────
st.subheader("🔥 Correlation Heatmap")

fig_heat, ax = plt.subplots(figsize=(5, 3))
corr = filtered_df.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

st.pyplot(fig_heat, use_container_width=False)

# ─────────────────────────────────────────────
# DOWNLOAD OPTION
# ─────────────────────────────────────────────
st.subheader("📥 Download Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv",
)

# ─────────────────────────────────────────────
# DATA TABLE
# ─────────────────────────────────────────────
st.subheader("📄 Data Preview")
st.dataframe(filtered_df)