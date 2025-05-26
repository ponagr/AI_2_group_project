import streamlit as st
from components.sidebar import render_sidebar
from components.filter_tab import filter_tab
from components.dashboard_views import plot_tab, metrics_view

st.set_page_config(page_title="Analytics by Occupation", layout="wide")

st.title("Analytics by Occupation")

df = render_sidebar()

filtered_df = filter_tab(df)

metrics_view(filtered_df, "Occupation Group")
plot_tab(filtered_df, "Occupation Group")