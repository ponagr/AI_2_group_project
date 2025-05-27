import streamlit as st
from components.sidebar import render_sidebar
from components.dashboard_views import desc_tab, show_newest_ads
from components.plots import plot_df
from utils.utils import aggregate_by_group


st.set_page_config(page_title="Overview", layout="wide")


df, field = render_sidebar()
if field == "Alla jobb":
    st.title("Overview")
else:
    st.title(f"Overview for {field}")


tab1, tab2 = st.tabs(["Plots", "Description"])
with tab1:
    df_new = show_newest_ads(df)
    # TODO gör om till en funktion med 3 tabs för bars, linjer och piechart
    if field == "Alla jobb":
        col = st.pills("select column:", ["Occupation Field", "Occupation Group", "Occupation", "Workplace City", "Employer Workplace", "Salary Description", "Duration", "Working Hours Type", "Driver License", "Experience Required"], default="Occupation Field", label_visibility="hidden")
    else:
        col = st.pills("select column:", ["Occupation Group", "Occupation", "Workplace City", "Employer Workplace", "Salary Description", "Duration", "Working Hours Type", "Driver License", "Experience Required"], default="Occupation Group", label_visibility="hidden")
    plot_df(aggregate_by_group(df_new, col), col)
with tab2:
    desc_tab(df_new)
    

