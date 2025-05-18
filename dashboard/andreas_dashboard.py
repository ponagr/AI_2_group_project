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
    
    # Filter the dataframe based on the selected date range
    filtered_date_df = df[(df["publication_date"] >= start_date) & (df["publication_date"] <= end_date)]
    
    # Group and sort the dataframe by occupation group and the sum of vacancies
    grouped_df = filtered_date_df.groupby("occupation_group", as_index=False)["vacancies"].sum()
    sorted_df = grouped_df.sort_values(by="vacancies", ascending=False)
    
    fig = px.bar(sorted_df, x="occupation_group", y="vacancies", labels={"occupation_group": "Occupation group", "vacancies":"Vacancies"})
    st.plotly_chart(fig)

def total_of_ads(df):
    st.title("Total number of ads")
    
    st.subheader(f"Total number of ads for 'occupation_field': {len(df)}")
    
    #filtered_date_df = get_date(df)
    grouped_df = df.groupby("occupation_group").size().reset_index(name="total_ads")
    sorted_df = grouped_df.sort_values(by="total_ads", ascending=False)
    
    fig = px.bar(sorted_df, x="occupation_group", y="total_ads", labels={"occupation_group": "Occupation group", "total_ads":"Total number of ads"})
    st.plotly_chart(fig)
    
def filter_layout(df):
    expander = st.expander("Filter")
    
    with expander:
        col1, col2 = st.columns(2)
        occupation_filter = col1.multiselect("Occupation", sorted(df["occupation_group"].unique()), default=[])
        city_filter = col1.multiselect("City", sorted(df['workplace_city'].unique()), default=[])
        employer_filter = col1.multiselect("Filter after employer", sorted(df["employer_workplace"].unique()), default=[])
        
        with col2:
            date_col1, date_col2 = st.columns(2)
            
            min_date = df["publication_date"].min().date()
            max_date = df["publication_date"].max().date()
            
            start_date = pd.to_datetime(date_col1.date_input("Start date", min_value=min_date, max_value=max_date, value=min_date))
            end_date = pd.to_datetime(date_col2.date_input("End date", min_value=start_date, max_value=max_date, value=max_date))
        
        license_required = st.pills("Requires drivers license", ["Yes", "No"], selection_mode="single")
        license_required = True if license_required == "Yes" else False if license_required == "No" else None
        
        # Apply filters
        filtered_df = df.copy()
        
        if occupation_filter:
            filtered_df = filtered_df[filtered_df["occupation_group"].isin(occupation_filter)]
        
        if city_filter:
            filtered_df = filtered_df[filtered_df["workplace_city"].isin(city_filter)]
        
        if employer_filter:
            filtered_df = filtered_df[filtered_df["employer_workplace"].isin(employer_filter)]
        
        filtered_df = filtered_df[(filtered_df["publication_date"] >= start_date) & (filtered_df["publication_date"] <= end_date)]
        
        if license_required is not None:
            filtered_df = filtered_df[filtered_df["driver_license"] == license_required]
        
    return filtered_df

def sideboard_menu():
    st.sidebar.title("Menu")
    
    pages = st.sidebar.radio("Select a page", options=[
        "Overview",
        "Analytics by occupation group",
        "Analytics by city",
        "Analytics by date",
        "Details" # Ha med?
    ])
    
    return pages

def vacancies_by_occupation(df):
    st.title("Vacancies by occupation")
    
    data_chart = group_and_sort(df, "occupation_group", "vacancies")
    fig = px.bar(data_chart, x="occupation_group", y="vacancies", labels={"occupation_group": "Occupation group", "vacancies": "Vacancies"})
    st.plotly_chart(fig)

def vacancies_by_city(df):
    st.title("Vacancies by city")
    
    data_chart = group_and_sort(df, "workplace_city", "vacancies")
    fig = px.bar(data_chart, x="workplace_city", y="vacancies", labels={"workplace_city": "City", "vacancies": "Vacancies"})
    st.plotly_chart(fig)

def vacancies_by_date(df):
    st.title("Vacancies by date")
    
    data_chart = group_and_sort(df, "publication_date", "vacancies")
    fig = px.bar(data_chart, x="publication_date", y="vacancies", labels={"publication_date": "Date", "vacancies": "Vacancies"})
    st.plotly_chart(fig)

def total_number_of_ads_by_occupation_group(df):
    st.title("Total number of ads by occupation group")
    
    data_chart = group_and_sort(df, "occupation_group", "vacancies", agg="count")
    fig = px.bar(data_chart, x="occupation_group", y="vacancies", labels={"occupation_group": "Occupation group", "vacancies": "Total number of ads"})
    st.plotly_chart(fig)

def group_and_sort(df, group_col, agg_col, agg="sum"):
    # Grouping the data by the group_col and aggregating the agg_col
    if agg == "sum":
        grouped_df = df.groupby(group_col)[agg_col].sum().reset_index()
    elif agg == "count":
        grouped_df = df.groupby(group_col)[agg_col].count().reset_index()
    else:
        raise ValueError("agg must be either sum or count")
    
    sorted_df = grouped_df.sort_values(by=agg_col, ascending=False)
    
    return sorted_df

def vacancy_details(df):
    st.title("Vacancy details")
    
    box = st.container(border=True)
    
    with box:
        col1, col2= st.columns(2)
        with col1:
            st.metric("Total Vacancies", int(df["vacancies"].sum()))
        with col2:
            most_vacant_occupation = df.groupby("occupation_group")["vacancies"].sum().idxmax()
            st.metric("Most Vacant Occupation", most_vacant_occupation)
        with col2:
            highest_vacancy_city = df.groupby("workplace_city")["vacancies"].sum().idxmax()
            st.metric("Highest Vacancy City", highest_vacancy_city)
        with col1:
            avg_vacancies_per_occupation = int(df.groupby("occupation_group")["vacancies"].sum().mean())
            st.metric("Avg Vacancies/Occupation", avg_vacancies_per_occupation)
        with col1:
            st.metric("Total Occupations", df["occupation_group"].nunique())
if __name__ == "__main__":
    query = "SELECT * FROM mart.mart_full_job_ads"
    df = load_data(query)
    filtered_df = filter_layout(df)
    total_of_ads(filtered_df)