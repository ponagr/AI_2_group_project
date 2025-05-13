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
    st.plotly_chart(fig)

if __name__ == "__main__":
    top_employer_occupation_group()