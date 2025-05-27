import streamlit as st
from components.sidebar import render_sidebar
from components.filter_tab import filter_tab
from components.dashboard_views import plot_tab, metrics_view

st.set_page_config(page_title="Analytics by Occupation", layout="wide")


df, field = render_sidebar()
if field == "Alla jobb":
    st.title("Analytics")
else:
    st.title(f"Analytics for {field}")

filtered_df = filter_tab(df)
choice = st.pills("Välj kolumn", ["Occupation Group", "Workplace City", "Employer Workplace", "Occupation"], selection_mode='single', default="Occupation Group", label_visibility="hidden")
metrics_view(filtered_df, choice)
plot_tab(filtered_df, choice)