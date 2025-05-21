import pandas as pd
import streamlit as st
from components.sidebar import render_sidebar
from components.filter_tab import filter_tab
from components.dashboard_views import desc_tab, plot_tab
from components.plots import barplot_df
from utils.utils import aggregate_by_group

st.set_page_config(page_title="Overview", layout="wide")

st.title("Overview")


df = render_sidebar()

tab1, tab2 = st.tabs(["Plots", "Description"])
with tab1:
    def show_newest_ads(df):
        df = df.sort_values("Publication Date", ascending=False).head(20).reset_index()
        expander = st.expander("20 latest job ads", expanded=True)
        expander.dataframe(df[["Occupation", "Employer Name", "Workplace City", "Publication Date"]])
        return df

    df_new = show_newest_ads(df)
    # TODO gör om till en funktion med 3 tabs för bars, linjer och piechart
    x = st.pills("select column:", ["Occupation Field", "Occupation Group", "Occupation", "Workplace City", "Employer Workplace", "Salary Description", "Duration", "Working Hours Type", "Driver License", "Experience Required"], default="Occupation Field", label_visibility="hidden")
    st.plotly_chart(barplot_df(aggregate_by_group(df_new, x), x, bar_ammount=20))
with tab2:
    desc_tab(df)