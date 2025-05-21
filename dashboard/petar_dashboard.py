import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

@st.cache_data
def load_dataset():
    query = "SELECT * FROM mart.mart_hotel_restaurant"
    return load_data(query)

df = load_dataset()


def sidebar_menu():
    st.sidebar.title("Meny")
    return st.sidebar.radio("Välj sektion:", ["Översikt", "Annonser per stad", "Exempelannonser"])


def show_kpi(df):
    st.subheader("Översikt")
    st.metric("Totalt antal annonser", len(df))


def show_vacancies_by_city(df):     
    st.subheader("Vacancies by City")
    # Group and sum vacancies by city
    grouped_df = df.groupby("workplace_city")["vacancies"].sum().reset_index()
    sorted_df = grouped_df.sort_values(by="vacancies", ascending=False)

    top_n = st.slider("Number of cities to display", min_value=5, max_value=20, value=10)

    fig = px.bar(       # Create bar chart
        sorted_df.head(top_n),
        x="workplace_city",
        y="vacancies",
        labels={"workplace_city": "City", "vacancies": "Number of Vacancies"},
        title="Top Cities by Job Vacancies"
    )

    st.plotly_chart(fig)