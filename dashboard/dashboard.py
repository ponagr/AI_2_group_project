import pandas as pd
import streamlit as st
from components.sidebar import render_sidebar
from components.filter_tab import filter_tab
from components.dashboard_views import desc_tab, show_newest_ads, plot_tab
from components.plots import barplot_df, lineplot_df, pieplot_df
from utils.utils import aggregate_by_group

st.set_page_config(page_title="Overview", layout="wide")

st.title("Overview")


df = render_sidebar()

tab1, tab2 = st.tabs(["Plots", "Description"])
with tab1:
    show_newest_ads(df)
    plot_tab(df)
with tab2:
    desc_tab(df)    
