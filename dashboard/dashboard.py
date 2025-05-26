import streamlit as st
from components.sidebar import render_sidebar
from components.dashboard_views import desc_tab
from components.plots import plot_df
from utils.utils import aggregate_by_group


def show_newest_ads(df):
    latest_date = df.sort_values("Publication Date", ascending=False).iloc[0]["Publication Date"]
    df = df[df["Publication Date"] == latest_date].reset_index()
    expander = st.expander(f"Total Ads: {len(df)} - ({latest_date.date()})", expanded=True)
    expander.dataframe(df[["Occupation", "Employer Name", "Workplace City"]])
    return df

st.set_page_config(page_title="Overview", layout="wide")

st.title("Overview")


df = render_sidebar()

tab1, tab2 = st.tabs(["Plots", "Description"])
with tab1:
    df_new = show_newest_ads(df)
    # TODO gör om till en funktion med 3 tabs för bars, linjer och piechart
    col = st.pills("select column:", ["Occupation Field", "Occupation Group", "Occupation", "Workplace City", "Employer Workplace", "Salary Description", "Duration", "Working Hours Type", "Driver License", "Experience Required"], default="Occupation Field", label_visibility="hidden")
    plot_df(aggregate_by_group(df_new, col), col)
with tab2:
    desc_tab(df)
    

