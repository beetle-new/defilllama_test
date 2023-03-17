import requests
import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(page_title="DeFiLlama TVL", page_icon="💰", layout="wide", initial_sidebar_state="collapsed",)

# Set up the API endpoint URL
url = 'https://api.flipsidecrypto.com/api/v2/queries/456bf6fe-078e-4cbb-987c-c3fbd6621202/data/latest'

# Send a GET request to the API endpoint
response = requests.get(url)

# Check if the response status code is 200 (OK)
if response.status_code == 200:
    
    # Load the response data into a pandas DataFrame
    data = pd.DataFrame(response.json())
    
    # Filter out the Wax chain
    data = data[data['CHAIN'] != 'Wax']
    
    # Define a function to create a chart with an expander containing the underlying data
    def create_chart_with_data(data, title):
        # Create the chart
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X('CHAIN:N', sort='-y'),
            y=alt.Y(f'{title.upper()}_CHANGE:Q'),
            color=alt.Color('CHAIN:N', legend=None)
        ).properties(
            title=title.title() + ' Change',
            width=500,
            height=500
        )
        # Create the data table
        data_table = data[['CHAIN', f'{title.upper()}_CHANGE']]
        return chart, data_table
    

    
    # Create the weekly change chart and data table
    weekly_chart, weekly_data = create_chart_with_data(data, 'weekly')
    
    # Create the monthly change chart and data table
    monthly_chart, monthly_data = create_chart_with_data(data, 'monthly')

# Set the app header
st.title("DeFi TVL Tracker")
st.write("Welcome to our DeFi TVL tracker! This tool provides real-time insights into the Total Value Locked (TVL) in USD within various DeFi protocols on Ethereum, Binance Smart Chain, Tron, and Arbitrum. Stay up-to-date with the latest DeFi trends and make informed investment decisions with our DeFi TVL tracker.")
st.write("Created by @1kbeetlejuice for Derek")
# Add some space for better readability
st.write("")
st.write("")

# Find the most negative and positive changes for each timeframe and the associated chain

weekly_min = weekly_data.loc[weekly_data['WEEKLY_CHANGE'].idxmin()]
weekly_max = weekly_data.loc[weekly_data['WEEKLY_CHANGE'].idxmax()]
monthly_min = monthly_data.loc[monthly_data['MONTHLY_CHANGE'].idxmin()]
monthly_max = monthly_data.loc[monthly_data['MONTHLY_CHANGE'].idxmax()]


# Display the changes with the most negative and positive values for each timeframe
beetlecol1, beetlecol2 = st.columns(2)
with beetlecol1:
    st.write(f"<h3 style='color: green;'>Largest Increase in Weekly TVL</h3><h4>{weekly_max['CHAIN']}: ${weekly_max['WEEKLY_CHANGE']:,.1f}</h4>", unsafe_allow_html=True)
with beetlecol2:
    st.write(f"<h3 style='color: red;'>Largest Decrease in Weekly TVL</h3><h4>{weekly_min['CHAIN']}: ${weekly_min['WEEKLY_CHANGE']:,.1f}</h4>", unsafe_allow_html=True)

nikkicol1, nikkicol2 = st.columns(2)
with nikkicol1:
    st.write(f"<h3 style='color: green;'>Largest Increase in Monthly TVL</h3><h4>{monthly_max['CHAIN']}: ${monthly_max['MONTHLY_CHANGE']:,.1f}</h4>", unsafe_allow_html=True)
with nikkicol2:
    st.write(f"<h3 style='color: red;'>Largest Decrease in Monthly TVL</h3><h4>{monthly_min['CHAIN']}: ${monthly_min['MONTHLY_CHANGE']:,.1f}</h4>", unsafe_allow_html=True)

ncol1, ncol2 = st.columns(2)
with ncol1:
    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
    tab1.subheader("Weekly Change")
    tab1.altair_chart(weekly_chart)
    tab2.subheader("Weekly Change Data")
    tab2.write(weekly_data)
    
with ncol2:
    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
    tab1.subheader("Monthly Change")
    tab1.altair_chart(monthly_chart)
    tab2.subheader("Monthly Change Data")
    tab2.write(monthly_data)
