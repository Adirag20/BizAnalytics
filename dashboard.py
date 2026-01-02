import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="BizAnalytica Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('sales_data.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("Data file 'sales_data.csv' not found. Please run 'data_generator.py' first.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filters")

# Region Filter
regions = ['All'] + sorted(df['Region'].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

# Category Filter
categories = ['All'] + sorted(df['Category'].unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Date Range Filter
min_date = df['Date'].min()
max_date = df['Date'].max()
start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Apply Filters
filtered_df = df.copy()
filtered_df = filtered_df[(filtered_df['Date'] >= pd.to_datetime(start_date)) & (filtered_df['Date'] <= pd.to_datetime(end_date))]

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

# Main Dashboard
st.title("📊 BizAnalytica Dashboard")

# KPIs
total_revenue = filtered_df['Total_Revenue'].sum()
total_profit = filtered_df['Total_Profit'].sum()
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
total_units = filtered_df['Units_Sold'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Profit Margin", f"{profit_margin:.1f}%")
col4.metric("Units Sold", f"{total_units:,}")

st.markdown("---")

# Charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Sales by Region")
    sales_by_region = filtered_df.groupby('Region')['Total_Revenue'].sum().reset_index()
    fig_region = px.bar(sales_by_region, x='Region', y='Total_Revenue', color='Region', title="Revenue by Region")
    st.plotly_chart(fig_region, use_container_width=True)

    st.subheader("Monthly Revenue Trend")
    monthly_sales = filtered_df.resample('M', on='Date')['Total_Revenue'].sum().reset_index()
    fig_trend = px.line(monthly_sales, x='Date', y='Total_Revenue', title="Monthly Revenue Trend", markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    st.subheader("Profit by Category")
    profit_by_category = filtered_df.groupby('Category')['Total_Profit'].sum().reset_index()
    fig_cat = px.pie(profit_by_category, values='Total_Profit', names='Category', title="Profit Distribution by Category", hole=0.4)
    st.plotly_chart(fig_cat, use_container_width=True)

    st.subheader("Top 5 Cities by Sales")
    top_cities = filtered_df.groupby('City')['Total_Revenue'].sum().sort_values(ascending=False).head(5).reset_index()
    fig_city = px.bar(top_cities, x='Total_Revenue', y='City', orientation='h', title="Top 5 Cities", color='Total_Revenue')
    st.plotly_chart(fig_city, use_container_width=True)

# Data Table
st.subheader("Detailed Data View")
st.dataframe(filtered_df.sort_values('Date', ascending=False).head(100))
