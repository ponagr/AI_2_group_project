import streamlit as st
from utils.utils import load_data

def render_sidebar():
    # Vyer för olika marts
    page = {
        "Alla jobb": "mart.mart_full_job_ads", 
        "Transport, Distribution, Lager": "mart.mart_transport_distrubution_layer",
        "Installation, Drift, Underhåll": "mart.mart_installation_maintenence",
        "Hotell, Restaurang, Storhushåll": "mart.mart_hotel_restaurant"
    }

    # Hämta df baserat på val av vy
    view_choice = st.sidebar.selectbox("Välj vy", list(page.keys()))
    
    df = load_data(page[view_choice])
    st.session_state["df"] = df
    
    box = st.sidebar.container()
    
    with box:
        col1, col2 = st.columns(2)
        # Visa en översikt av datan
        col1.metric("Total Job Ads", len(df))
        col2.metric("Total Vacancies", int(df["Vacancies"].sum()))
        
        avg_vacancies_per_occupation = int(df.groupby("Occupation")["Vacancies"].sum().mean())
        col1.metric("Avg Vacancies/Occupation", avg_vacancies_per_occupation)
        
        avg_vacancies_per_employer = int(df.groupby("Employer Name")["Vacancies"].sum().mean())
        col2.metric("Avg Vacancies/Employer", avg_vacancies_per_employer)
        
        most_vacant_occupation = df.groupby("Occupation")["Vacancies"].sum().idxmax()
        st.sidebar.metric("Most Vacant Occupation", most_vacant_occupation)
        
        highest_vacancy_city = df.groupby("Workplace City")["Vacancies"].sum().idxmax()
        st.sidebar.metric("Highest Vacancy City", highest_vacancy_city)
        
        highest_vacancy_employer = df.groupby("Employer Name")["Vacancies"].sum().idxmax()
        st.sidebar.metric("Highest Vacancy Employer", highest_vacancy_employer)
    
    return df