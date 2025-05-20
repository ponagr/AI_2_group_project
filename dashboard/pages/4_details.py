import streamlit as st
import pandas as pd
import plotly.express as px
from sidebar import render_sidebar
from filter_tab import filter_tab

st.set_page_config(page_title="Details", layout="wide")

st.title("Details")

df = render_sidebar()

filtered_df = filter_tab(df)