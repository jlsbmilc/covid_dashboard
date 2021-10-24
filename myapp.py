import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date


st.set_page_config(page_title="JL COVID dashboard")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

df_raw = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
cols = [s for s in list(df_raw.columns) if "total" in s]
other_cums = ["stringency_index", "people_fully_vaccinated"]
cols = [*cols, *other_cums]
df_totals = df_raw.groupby(['location'])[cols].ffill().fillna(0).astype(int)
df_raw.drop(columns=list(df_totals.columns),inplace=True)
df_raw = pd.merge(df_raw, df_totals, left_index=True, right_index=True)


st.title("COVID19  dashboard")
st.write("Data was retrieved from: https://github.com/owid/covid-19-data/tree/master/public/data")
st.write("All data used in this app belongs to authors listed below:")
st.write("*Hannah Ritchie, Edouard Mathieu, Lucas Rodés-Guirao, Cameron Appel, Charlie Giattino, Esteban Ortiz-Ospina,Joe Hasell, Bobbie Macdonald, Diana Beltekian and Max Roser (2020) - \"Coronavirus Pandemic (COVID-19)\". Published online at OurWorldInData.org. Retrieved from: 'https://ourworldindata.org/coronavirus' [Online Resource]*")

locations = list(df_raw['location'].unique())
macro_locations = ['Europe', 'European Union', 'World', 'Africa', 'Asia']
micro_locations = [item for item in locations if item not in macro_locations]
region_type = st.sidebar.radio("Select a region type:", ['Macro', 'Country'],index=1)

if region_type == 'Macro':
    locations = pd.Series(macro_locations)
    default_index = macro_locations.index("World")
else:
    locations = pd.Series(micro_locations)
    default_index = micro_locations.index("Poland")

selection = st.sidebar.selectbox('Please select a location:', locations, index = default_index)
data = df_raw[df_raw['location'] == selection]
data['date_val'] = data['date'].apply(lambda x: date.fromisoformat(x))
first_day = data['date_val'].min()
last_day = data['date_val'].max()

##Location info

population = int(data['population'].unique()[0])
total_cases = int(data['total_cases'].iloc[-1])
people_vaccinated = int(data['people_fully_vaccinated'].iloc[-1])
last_stringency_index = data['stringency_index'].iloc[-1]

st.sidebar.write("Location:", selection)
st.sidebar.write("Population:", f"{population:,}")
st.sidebar.write("Last date reported:", last_day)
st.sidebar.write("Total cases:", f"{total_cases:,}")
st.sidebar.write("People fully vaccinated:", f"{people_vaccinated:,}")
st.sidebar.write("Current stringency index (0-100):", last_stringency_index)

st.subheader("Figure 1. Cumulative and daily COVID19 cases in time")
st.subheader("Location: "+selection)

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Bar(x=data['date'], y=data['new_cases_smoothed'], name="Daily new cases in time",marker=dict(color='blue',line=dict(color='blue'))),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=data['date'], y=data['total_cases'], name="Total cases in time", mode='lines', marker=dict(color='red',line=dict(color='red'))),
    secondary_y=True
)
st.plotly_chart(fig)


st.subheader("Figure 2. COVID cases in time daily and stringency level")
st.subheader("Location: "+selection)
fig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2.add_trace(
    go.Bar(x=data['date'], y=data['new_cases_smoothed'], name="Daily new cases in time", marker=dict(color='blue',line=dict(color='blue'))),
    secondary_y=False
)
fig2.add_trace(
    go.Scatter(x=data['date'], y=data['stringency_index'], name="Stringency index in time", mode='lines', marker=dict(color='red',line=dict(color='red'))),
    secondary_y=True
)
st.plotly_chart(fig2)


st.subheader("What is correlated with death rate?")

st.write("Lethality defined as:")
st.latex(r'''
lethality = \frac{\text{new deaths}}{\text{new cases}}
''')

selected_country = selection
data_leth = df_raw[df_raw['location'] == selection]
data_leth = data_leth[data_leth['total_cases'] != 0]
data_leth['lethality'] = data_leth.apply(lambda row: row['total_deaths']/row['total_cases'], axis=1)

considered_factors = ['total_cases', 'new_cases',
       'new_cases_smoothed', 'total_deaths', 'new_deaths',
       'new_deaths_smoothed', 'total_cases_per_million',
       'new_cases_per_million', 'new_cases_smoothed_per_million',
       'total_deaths_per_million', 'new_deaths_per_million',
       'new_deaths_smoothed_per_million', 'reproduction_rate', 'icu_patients',
       'icu_patients_per_million', 'hosp_patients',
       'hosp_patients_per_million', 'weekly_icu_admissions',
       'weekly_icu_admissions_per_million', 'weekly_hosp_admissions',
       'weekly_hosp_admissions_per_million', 'new_tests', 'total_tests',
       'total_tests_per_thousand', 'new_tests_per_thousand',
       'new_tests_smoothed', 'new_tests_smoothed_per_thousand',
       'positive_rate', 'tests_per_case', 'tests_units', 'total_vaccinations',
       'people_vaccinated', 'people_fully_vaccinated', 'total_boosters',
       'new_vaccinations', 'new_vaccinations_smoothed',
       'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred',
       'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred',
       'new_vaccinations_smoothed_per_million', 'stringency_index']

selected_factor = st.selectbox("Select a factor:", considered_factors,index=considered_factors.index("people_fully_vaccinated"))

st.subheader("Figure 3. Lethality in time vs "+selected_factor)
st.subheader("Location: "+selection)

fig3 = make_subplots(specs=[[{"secondary_y": True}]])
fig3.add_trace(
    go.Scatter(x=data_leth['date'], y=data_leth['lethality'], name = 'lethality', mode='lines', marker=dict(color='blue',line=dict(color='blue'))),
    secondary_y=False
)
fig3.add_trace(
    go.Scatter(x=data_leth['date'], y=data_leth[selected_factor], name = selected_factor, mode='lines', marker=dict(color='red',line=dict(color='red'))),
    secondary_y=True 
)
st.plotly_chart(fig3)

df_cum = df_raw[df_raw['location'].isin(micro_locations)]
df_cum = df_cum.groupby(['location']).max().reset_index()

st.subheader("Figure 4. Total cases per country")
fig4 = px.choropleth(df_cum, locations = 'iso_code', color='total_cases_per_million', hover_name = df_cum['location'], color_continuous_scale="Peach", projection = 'natural earth')
st.plotly_chart(fig4)