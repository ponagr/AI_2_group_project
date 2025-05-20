import pandas as pd
import streamlit as st
from components.sidebar import render_sidebar
from components.filter_tab import filter_tab
from components.dashboard_views import desc_tab, plot_tab


st.set_page_config(page_title="Overview", layout="wide")

st.title("Overview")


df = render_sidebar()

filtered_df = filter_tab(df)

tab1, tab2 = st.tabs(["Plots", "Description"])
with tab1:
    plot_tab(filtered_df)
with tab2:
    desc_tab(filtered_df)
