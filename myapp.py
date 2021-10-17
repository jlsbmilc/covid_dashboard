import streamlit as st
import pandas as pd
import plotly.express as px

df_raw = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")

st.title("Covid dashboard")
locations = pd.Series(df_raw['location'].unique())
selection = st.selectbox('Please select a location:', locations)

data = df_raw[df_raw['location'] == selection]
fig = px.line(data, x='date', y='total_cases')
fig2 = px.bar(data, x='date', y='new_cases')
# fig.add_trace(fig2)
st.plotly_chart(fig)

st.plotly_chart(fig2)