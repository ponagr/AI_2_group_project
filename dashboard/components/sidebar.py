import streamlit as st
from utils import load_data

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
    
    # Visa en översikt av datan
    st.sidebar.metric("Total Vacancies", int(df["Vacancies"].sum()))
    
    most_vacant_occupation = df.groupby("Occupation")["Vacancies"].sum().idxmax()
    st.sidebar.metric("Most Vacant Occupation", most_vacant_occupation)
    
    highest_vacancy_city = df.groupby("Workplace City")["Vacancies"].sum().idxmax()
    st.sidebar.metric("Highest Vacancy City", highest_vacancy_city)
    
    avg_vacancies_per_occupation = int(df.groupby("Occupation")["Vacancies"].sum().mean())
    st.sidebar.metric("Avg Vacancies/Occupation", avg_vacancies_per_occupation)
    
    st.sidebar.metric("Total Occupations", df["Occupation"].nunique())
    
    return df