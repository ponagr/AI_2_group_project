import streamlit as st
from utils.utils import aggregate_by_group
from components.kpis import show_metrics

import plotly.express as px

def metrics_view(df, column=None):
    df = df[df[column] != "Ej Angiven"]
    df = aggregate_by_group(df, column)
    if column is not None:
        st.markdown(f"## Top 5: {column}s")
        show_metrics(df, column, "Vacancies", 5)

def plot_tab(df, column=None):
    bar, line, pie = st.tabs(["Barchart", "Linechart", "Piechart"])
    
    df = df[(df[column] != "Ej Angiven") & (df[column] != "Not Specified") & (df[column] != "Undefined")]
    
    line_chart_df = df.groupby(["Publication Date", column]).size().reset_index(name="Total Ads")
    line_chart_df = line_chart_df[line_chart_df["Publication Date"] > 5]
    
    df = aggregate_by_group(df, column)
    num_groups = st.slider("Number of groups to show", min_value=1, max_value=10, value=5)
    with bar:
        st.markdown("### Total vacancies for top " + str(num_groups) + " " + column)
        fig = px.bar(df.head(num_groups), x=column, y="Vacancies", color=column)
        st.plotly_chart(fig)
    
    with line:
        st.markdown(f"### Total job ads over time by {column}")
        fig = px.line(line_chart_df, x="Publication Date", y="Total Ads", color=column, line_shape='linear')
        fig.update_layout(
            template="plotly_white",  # ren stil
            hovermode="x unified",  # samlad hover-info
            margin=dict(l=20, r=20, t=60, b=40),
            height=500,
        )
        fig.update_xaxes(
            tickformat="%Y-%m-%d",  # YYYY-MM-DD
            tickangle=45,
            showgrid=True
        )
        st.plotly_chart(fig)
    
    with pie:
        st.markdown("### Total vacancies for top " + str(num_groups) + " " + column)
        df = aggregate_by_group(df, column)
        fig = px.pie(df.head(num_groups), values="Vacancies", names=column, color=column)
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