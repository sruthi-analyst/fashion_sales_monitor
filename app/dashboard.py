import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Fashion Retail Sales Monitor ")

DATA_PATH = "S:/Sri Eshwar Acad/I - II/Python/fashion_sales_monitor/data/sample.xlsx"

@st.cache_data
def load_data(path):
    df = pd.read_excel(path, engine='openpyxl')
    df.dropna(inplace=True)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['TotalPrice'] = df['Quantity'] * df['Price']
    df['Month'] = df['InvoiceDate'].dt.month
    return df

df = load_data(DATA_PATH)

# Bar Chart: Sales by Product Description
st.subheader("Sales by Product Description")
category_sales = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)
st.bar_chart(category_sales)

# Line Plot: Monthly Revenue Trend
st.subheader("Monthly Revenue Trend")
monthly_revenue = df.groupby('Month')['TotalPrice'].sum()
st.line_chart(monthly_revenue)

# Heatmap: Returns by Product and Month
st.subheader("Returns Heatmap (Top Products)")
returns = df[df['Quantity'] < 0]
pivot = returns.pivot_table(index='Description', columns='Month', values='Quantity', aggfunc='sum', fill_value=0)
pivot = pivot.loc[pivot.sum(axis=1).abs().sort_values(ascending=False).head(10).index]
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot, cmap="YlOrRd", annot=True, fmt=".0f", ax=ax)
st.pyplot(fig)
