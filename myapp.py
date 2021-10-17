import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df_raw = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")

st.title("Covid dashboard")
locations = pd.Series(df_raw['location'].unique())
selection = st.selectbox('Please select a location:', locations)

data = df_raw[df_raw['location'] == selection]
fig = px.line(data, x='date', y='total_cases')
fig2 = px.bar(data, x='date', y='new_cases')
st.plotly_chart(fig)

st.plotly_chart(fig2)

fig3 = make_subplots(specs=[[{"secondary_y": True}]])


fig3.add_trace(
    go.Bar(x=data['date'], y=data['new_cases'], name="Daily new cases in time"),
    secondary_y=False
)

fig3.add_trace(
    go.Scatter(x=data['date'], y=data['stringency_index'], name="Stringency index in time", mode='lines'),
    secondary_y=True
)


st.write("Chart 3")

st.plotly_chart(fig3)