import streamlit as st
import pandas as pd
from utils.utils import get_sorted_group_labels, filter_df, aggregate_by_group
from components.kpis import show_metrics

import plotly.express as px

def metrics_view(df, column=None):
    if column is not None:
        st.markdown(f"## Top 5: {column}s")
        show_metrics(df, column, "Vacancies", 5)

def plot_tab(df, column=None):
    
    bar, line, pie = st.tabs(["Barchart", "Linechart", "Piechart"])
    line_chart_df = df.groupby(["Publication Date", "Occupation Field"]).size().reset_index(name="Total Ads")
    
    if column is None:
        line_chart_df = df.groupby(["Publication Date", "Occupation Field"]).size().reset_index(name="Total Ads")
        with bar:
            st.markdown("### Vad ska vi ha för diagram?")

        with line:
            # lineplot total job ads for each occupation field by publication date
            st.markdown("### Total job ads for each occupation field by publication date")
            fig = px.line(line_chart_df, x="Publication Date", y="Total Ads", color="Occupation Field")
            st.plotly_chart(fig)
        
        with pie:
            # piechart total vacancies by occupation field
            st.markdown("### Total vacancies by occupation field")
            df = aggregate_by_group(df, "Occupation Field")
            fig = px.pie(df, values="Vacancies", names="Occupation Field")
            st.plotly_chart(fig)
    elif column != "Publication Date":
        line_chart_df = df.groupby(["Publication Date", column]).size().reset_index(name="Total Ads")
        df = aggregate_by_group(df, column)
        num_groups = st.slider("Number of groups to show", min_value=1, max_value=10, value=5)
        with bar:
            st.markdown("### Total vacancies for top " + str(num_groups) + " " + column)
            fig = px.bar(df.head(num_groups), x=column, y="Vacancies")
            st.plotly_chart(fig)
        
        with line:
            st.markdown("### Total job ads for top " + str(num_groups) + " " + column + " by publication date")
            fig = px.line(line_chart_df.head(num_groups), x="Publication Date", y="Total Ads", color=column)
            st.plotly_chart(fig)
        
        with pie:
            st.markdown("### Total vacancies for top " + str(num_groups) + " " + column)
            df = aggregate_by_group(df, column)
            fig = px.pie(df.head(num_groups), values="Vacancies", names=column)
            st.plotly_chart(fig)

def desc_tab(df):
    st.markdown("### Jobbannonsbeskrivning")
    
    # Selectbox för Headline
    headline = st.selectbox("Matchade jobbannonser baserad på filtrering:",["Välj jobbannons"] + df["Headline"].unique().tolist())
    job_ad = df[df["Headline"] == headline]
    
    # Annonsbeskrivning för Headline
    if headline == "Välj jobbannons":
        st.info("Välj en jobbannons för beskrivning")
    else:
        st.dataframe(job_ad[["Employer Name", "Employer Workplace", "Workplace City", "Duration", "Working Hours Type"]])
        st.info(job_ad[job_ad["Description"].notnull()].iloc[0]["Description"])