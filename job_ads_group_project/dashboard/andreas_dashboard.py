import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

def top_employer_occupation_group():
    st.title("Top employers by occupation group")
    query = "SELECT employer_name, vacancies, occupation_group FROM mart.mart_installation_maintenence"
    df = load_data(query)
    
    # Create a selectbox for the occupation group and filter the dataframe based on the selection
    occupation_group = st.selectbox("Occupation group", ["All"] + list(df["occupation_group"].unique()))
    if occupation_group != "All":
        filtered_df = df[df["occupation_group"] == occupation_group]
    
    # Create a slider for top N employwers to display
    top_employer = st.slider("Top N employers", 1, 10, 5)
    
    # Group and sort the dataframe by empolyer name and the sum of vacancies
    grouped_df = filtered_df.groupby("employer_name", as_index=False)["vacancies"].sum()
    sorted_df = grouped_df.sort_values(by="vacancies", ascending=False)
    
    fig = px.bar(sorted_df.head(top_employer), x="employer_name", y="vacancies", labels={"employer_name":"Employer name"})
    st.plotly_chart(fig)

def total_vacancies_by_date():
    st.title("Total vacancies by date")
    query = "SELECT publication_date, vacancies, occupation_group FROM mart.mart_installation_maintenence"
    df = load_data(query)
    
    #  Set min and max date for the date input to the min and max date from the data
    min_date = df["publication_date"].min().date()
    max_date = df["publication_date"].max().date()
    
    # Create a date input for the start and end date
    start_date = st.date_input("Start date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("End date", min_value=min_date, max_value=max_date, value=max_date)
    
    # Convert the start and end date to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Filter the dataframe based on the selected date range
    filtered_date_df = df[(df["publication_date"] >= start_date) & (df["publication_date"] <= end_date)]
    
    # Group and sort the dataframe by occupation group and the sum of vacancies
    grouped_df = filtered_date_df.groupby("occupation_group", as_index=False)["vacancies"].sum()
    sorted_df = grouped_df.sort_values(by="vacancies", ascending=False)
    
    fig = px.bar(sorted_df, x="occupation_group", y="vacancies", labels={"occupation_group": "Occupation group", "vacancies":"Vacancies"})
    st.plotly_chart(fig)

def total_of_ads():
    st.title("Total number of ads")
    query = "SELECT COUNT(*) AS total_ads, publication_date, occupation_group FROM mart.mart_installation_maintenence GROUP BY publication_date, occupation_group"
    df = load_data(query)
    
    st.subheader(f"Total number of ads for 'occupation_field': {df['total_ads'].sum()}")
    
    min_date = df["publication_date"].min().date()
    max_date = df["publication_date"].max().date()
    
    start_date = st.date_input("Start date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("End date", min_value=start_date, max_value=max_date, value=max_date)
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    filtered_date_df = df[(df["publication_date"] >= start_date) & (df["publication_date"] <= end_date)]
    grouped_df = filtered_date_df.groupby("occupation_group").size().reset_index(name="total_ads")
    sorted_df = grouped_df.sort_values(by="total_ads", ascending=False)
    
    fig = px.bar(sorted_df, x="occupation_group", y="total_ads", labels={"occupation_group": "Occupation group", "total_ads":"Total number of ads"})
    st.plotly_chart(fig)
    
if __name__ == "__main__":
    #top_employer_occupation_group()
    total_vacancies_by_date()