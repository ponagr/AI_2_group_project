import streamlit as st
import pandas as pd
import plotly.express as px
from components.sidebar import render_sidebar
from components.filter_tab import filter_tab
from components.dashboard_views import desc_tab, plot_tab

st.set_page_config(page_title="Analytics by Occupation", layout="wide")

st.title("Analytics by Occupation")

df = render_sidebar()

filtered_df = filter_tab(df)

tab1, tab2 = st.tabs(["Plots", "Description"])
with tab1:
    plot_tab(filtered_df, "Occupation Group")
with tab2:
    desc_tab(filtered_df)