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

def apply_filters(df):
    st.sidebar.subheader("Filter by City")
    cities = st.sidebar.multiselect("Choose city/cities", sorted(df["workplace_city"].dropna().unique()))
    if cities:
        df = df[df["workplace_city"].isin(cities)]
    return df


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

def show_top_ads(df):
    st.subheader("Example Job Ads")
    st.dataframe(df[["headline", "employer_name", "workplace_city", "publication_date"]].head(10))


def main():
    section = sidebar_menu()
    filtered_df = apply_filters(df)

    if section == "Overview":
        show_kpi(filtered_df)
    elif section == "Vacancies by City":
        show_vacancies_by_city(filtered_df)
    elif section == "Example Job Ads":
        show_top_ads(filtered_df)


if __name__ == "__main__":
    main()