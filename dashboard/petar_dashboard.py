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