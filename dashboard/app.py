import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('data/processed/cleaned_spending.csv')
df['date'] = pd.to_datetime(df['date'])

st.title("Consumer Spending Trends Dashboard")
st.markdown("Filter and explore consumer spending patterns interactively.")

# Sidebar filters
st.sidebar.header("Filters")

# Filter by category
categories = df['category'].dropna().unique().tolist()
selected_category = st.sidebar.multiselect('Category', categories, default=categories)

# Filter by location
locations = df['location'].dropna().unique().tolist()
selected_location = st.sidebar.multiselect('Location', locations, default=locations)

# Filter by date range
min_date = df['date'].min()
max_date = df['date'].max()
date_range = st.sidebar.date_input('Date range', [min_date, max_date])

# Filter data
filtered = df[
    (df['category'].isin(selected_category)) &
    (df['location'].isin(selected_location)) &
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1]))
]

st.write(f"### Showing {len(filtered)} transactions")

# Summary stats
st.metric("Total Spend ($)", f"{filtered['spend_amount'].sum():,.2f}")
st.metric("Average Spend ($)", f"{filtered['spend_amount'].mean():,.2f}")

# Bar chart: total spend by category
if not filtered.empty:
    bar_data = filtered.groupby('category')['spend_amount'].sum().reset_index()
    bar_fig = px.bar(bar_data, x='category', y='spend_amount', title='Total Spend by Category')
    st.plotly_chart(bar_fig)

    # Pie chart: spend by payment method
    pie_data = filtered.groupby('payment_method')['spend_amount'].sum().reset_index()
    pie_fig = px.pie(pie_data, names='payment_method', values='spend_amount', title='Spend by Payment Method')
    st.plotly_chart(pie_fig)

    # Line chart: spend over time
    time_data = filtered.groupby('date')['spend_amount'].sum().reset_index()
    line_fig = px.line(time_data, x='date', y='spend_amount', title='Spend Over Time')
    st.plotly_chart(line_fig)

else:
    st.warning("No data for selected filters.")

st.markdown("Project by **Armando Gomez** | Data: Synthetic for demonstration")
