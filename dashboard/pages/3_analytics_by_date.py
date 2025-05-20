import streamlit as st
import pandas as pd
import plotly.express as px
from components.sidebar import render_sidebar
from components.filter_tab import filter_tab

st.set_page_config(page_title="Analytics by date", layout="wide")

st.title("Analytics by date")

df = render_sidebar()

filtered_df = filter_tab(df)