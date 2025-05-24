import streamlit as st
from utils.utils import aggregate_by_group
from components.kpis import show_metrics
from components.plots import barplot_df, lineplot_df, pieplot_df

import plotly.express as px

def metrics_view(df, column=None):
    df = df[df[column] != "Ej Angiven"]
    df = aggregate_by_group(df, column)
    if column is not None:
        st.markdown(f"## Top 5: {column}s")
        show_metrics(df, column, "Vacancies", 5)

def show_newest_ads(df):
        df = df.sort_values("Publication Date", ascending=False).head(20).reset_index()
        expander = st.expander("20 latest job ads", expanded=True)
        expander.dataframe(df[["Occupation", "Employer Name", "Workplace City", "Publication Date"]])

def plot_tab(df, column=None):
    columns = ["Occupation Field", "Occupation Group", "Occupation",
                "Workplace City", "Employer Workplace", "Salary Description",
                "Duration", "Working Hours Type", "Driver License", "Experience Required"]
    
    if column is None:
        selection = st.pills("select column:", columns, default="Occupation Field", label_visibility="hidden")
        
        if selection == "Occupation Field":
            vacancies_over_time_df = df.groupby("Publication Date").size().reset_index(name="Vacancies")
            color_col = None
        else:
            vacancies_over_time_df = df.groupby(["Publication Date", selection]).size().reset_index(name="Vacancies")
            color_col = selection
        
        df = aggregate_by_group(df, selection)
        
        bar, line, pie = st.tabs(["Barchart", "Linechart", "Piechart"])
        with bar:
            barplot_df(df, selection)
        
        with line:
            lineplot_df(vacancies_over_time_df, x_column="Publication Date", y_column="Vacancies", color_column=color_col)
        
        with pie:  
            pieplot_df(df, selection)
    
    else:
        line_chart_df = df.groupby(["Publication Date", column]).size().reset_index(name="Total Ads")
        df = aggregate_by_group(df, column)
        
        bar, line, pie = st.tabs(["Barchart", "Linechart", "Piechart"])
        num_groups = st.slider("Number of groups to show", min_value=1, max_value=10, value=5)
        with bar:
            barplot_df(df, column, y_column="Vacancies", bar_ammount=num_groups)
        
        with line:
            lineplot_df(line_chart_df, x_column="Publication Date", y_column="Total Ads", color_column=column)
        
        with pie:
            pieplot_df(df, column, y_column="Vacancies", bar_ammount=num_groups)

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