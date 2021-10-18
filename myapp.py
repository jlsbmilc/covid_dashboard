import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date

df_raw = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")

st.title("COVID19  dashboard")
st.write("Data was retrieved from: https://github.com/owid/covid-19-data/tree/master/public/data")
st.write("All data used in this app belongs to authors listed below:")
st.write("*Hannah Ritchie, Edouard Mathieu, Lucas Rodés-Guirao, Cameron Appel, Charlie Giattino, Esteban Ortiz-Ospina,Joe Hasell, Bobbie Macdonald, Diana Beltekian and Max Roser (2020) - \"Coronavirus Pandemic (COVID-19)\". Published online at OurWorldInData.org. Retrieved from: 'https://ourworldindata.org/coronavirus' [Online Resource]*")

locations = pd.Series(df_raw['location'].unique())

selection = st.sidebar.selectbox('Please select a location:', locations)
data = df_raw[df_raw['location'] == selection]
data['date_val'] = data['date'].apply(lambda x: date.fromisoformat(x))
first_day = data['date_val'].min()
last_day = data['date_val'].max()
chosen_date = st.sidebar.slider("Choose a date:", min_value = first_day, max_value = last_day, value=last_day)
data = data.loc[data['date_val']<=chosen_date]

st.subheader("Figure 1. COVID19 cases in time - cumulative")
fig = px.line(data, x='date', y='total_cases')
st.plotly_chart(fig)

st.subheader("Figure 2. COVID19 cases in time - daily")
fig2 = px.bar(data, x='date', y='new_cases')
st.plotly_chart(fig2)


st.subheader("Figure 3. COVID cases in time daily and stringency level")
fig3 = make_subplots(specs=[[{"secondary_y": True}]])
fig3.add_trace(
    go.Bar(x=data['date'], y=data['new_cases'], name="Daily new cases in time"),
    secondary_y=False
)
fig3.add_trace(
    go.Scatter(x=data['date'], y=data['stringency_index'], name="Stringency index in time", mode='lines'),
    secondary_y=True
)
st.plotly_chart(fig3)

st.subheader("Figure 4. New cases vs. stringency index")
fig4 = px.scatter(data, x='new_cases', y='stringency_index')
st.plotly_chart(fig4)