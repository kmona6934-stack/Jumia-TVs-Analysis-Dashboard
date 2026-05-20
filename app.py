import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Jumia TV Analytics")

st.title("📺 Jumia Smart TVs Analytics Dashboard")
st.markdown("An interactive web application to analyze pricing dynamics and discounts across TV brands.")
st.markdown("---")

df = pd.read_csv('jumia_SmartTVs_Report.csv')
df['Discount_Num'] = df['Discount'].str.replace('%', '').astype(float) / 100
df['Original_Price'] = df['Price (EGP)'] / (1 - df['Discount_Num'])
df['Discount_Value'] = df['Original_Price'] - df['Price (EGP)']

st.sidebar.header("Filter Settings")
brands = sorted(df['Brand'].unique())
selected_brand = st.sidebar.selectbox("Select TV Brand:", brands)

filtered_df = df[df['Brand'] == selected_brand]

st.subheader(f"📊 Key Performance Indicators for: {selected_brand}")
col1, col2, col3 = st.columns(3)

with col1:
    avg_price = filtered_df['Price (EGP)'].mean()
    st.metric(label="Average Selling Price (EGP)", value=f"{avg_price:,.0f}")

with col2:
    max_discount_val = filtered_df['Discount_Value'].max()
    st.metric(label="Max Discount Value Available (EGP)", value=f"{max_discount_val:,.0f}")

with col3:
    avg_discount_pct = filtered_df['Discount_Num'].mean() * 100
    st.metric(label="Average Discount Percentage (%)", value=f"{avg_discount_pct:.1f}%")

st.markdown("---")

left_chart, right_table = st.columns([3, 2])

with left_chart:
    st.subheader("🎯 Price vs Discount Value Analysis")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(
        data=filtered_df, 
        x='Price (EGP)', 
        y='Discount_Value', 
        size='Discount_Num', 
        sizes=(50, 300),
        ax=ax,
        color='#4CAF50'
    )
    ax.set_title(f'Discount Value vs Current Price for {selected_brand}', fontsize=12)
    ax.set_xlabel('Current Price (EGP)', fontsize=10)
    ax.set_ylabel('Discount Amount (EGP)', fontsize=10)
    
    st.pyplot(fig)

with right_table:
    st.subheader("📋 Product Data View")
    st.dataframe(
        filtered_df[['Product Name', 'Price (EGP)', 'Discount']].head(10),
        use_container_width=True
    )