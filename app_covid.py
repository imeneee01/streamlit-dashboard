import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json

def main():
    st.title("Tableau de bord interactif COVID-19")
    st.sidebar.header("Options de sélection")
    
    data = pd.read_csv('covid_data.csv')

    st.sidebar.title("Séléction liées à l'évolution des cas")
    countries = sorted(data["name"].dropna().unique())
    selected_countries = st.sidebar.multiselect("Sélectionner un ou plusieurs pays", countries)
    
    case_type = st.sidebar.selectbox("Sélectionner le type de cas", ("Confirmés", "Décès", "Guéris"))
    st.sidebar.title("Séléction liées au décès dans le monde")
    available_dates = sorted(data["date"].unique())
    selected_date = st.sidebar.selectbox("Sélectionner une date", available_dates)
    
    filtered_data = data[data["name"].isin(selected_countries)]

    grouped_data = filtered_data.groupby(["date", "name"]).agg(
        confirmed=('confirmed', 'sum'),
        deaths=('deaths', 'sum'),
        recovered=('recovered', 'sum')
    ).reset_index()
    
    total_cases = grouped_data["confirmed"].sum()
    total_deaths = grouped_data["deaths"].sum()
    total_recovered = grouped_data["recovered"].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Cas confirmés", f"{total_cases:,}")
    col2.metric("Décès", f"{total_deaths:,}")
    col3.metric("Guérisons", f"{total_recovered:,}")
    
    if case_type == "Confirmés":
        fig = px.line(grouped_data, x="date", y="confirmed", color="name", title="Évolution des cas confirmés", markers=True)
    elif case_type == "Décès":
        fig = px.line(grouped_data, x="date", y="deaths", color="name", title="Évolution des décès", markers=True)
    else:
        fig = px.line(grouped_data, x="date", y="recovered", color="name", title="Évolution des guérisons", markers=True)
    
    st.plotly_chart(fig)
    
    st.subheader("Distribution géographique des décès")
    
    map_data = data[data["date"] == selected_date]
    
    fig_map = px.choropleth(
        map_data,
        locations="iso",
        color="deaths",
        hover_name="name",
        color_continuous_scale="Reds",
        title=f"Distribution des décès le {selected_date}",
        width=600,
        height=700
    )
    
    st.plotly_chart(fig_map)

if __name__ == "__main__":
    main()
