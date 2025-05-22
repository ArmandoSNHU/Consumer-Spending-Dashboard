import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('../data/processed/cleaned_spending.csv')

st.title("Consumer Spending Trends Dashboard")

# Filter
category = st.selectbox("Choose category", sorted(df['category'].unique()))
filtered = df[df['category'] == category]

# Plot
fig = px.line(filtered, x="date", y="spend_amount", title=f"{category} Spending Over Time")
st.plotly_chart(fig)
