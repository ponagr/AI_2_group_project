import streamlit as st
from utils.utils import aggregate_by_group
from components.kpis import show_metrics
from gemini.llm import summarize_description
from datetime import date, timedelta
import plotly.express as px

# function for filtering by new ads or ads with last day applications showing the dataframe
def show_ads(df, choice):
    if choice == "Application deadline today":
        col = "Application Deadline"
    else:
        col = "Publication Date"
    
    # getting todays date to filter df with choice in Overview page
    today = str(date.today())
    df_today = df[df[col] == today].reset_index()
    
    if len(df_today) == 0:
        if col == "Publication Date":
            latest_date = df[col].max()
            df = df[df[col] == latest_date].reset_index()
            st.markdown(f"### Total Ads: {len(df)}")
            st.markdown(f"#### Date: {latest_date.date()}")
            expander = st.expander(f"Total Ads: {len(df)} - ({latest_date.date()})", expanded=True)
        else:
            tomorrow = str(date.today() + timedelta(days=1))
            df = df[df[col] == tomorrow].reset_index()
            st.markdown(f"### Total Ads: {len(df)}")
            st.markdown(f"#### Date: {tomorrow}")
            expander = st.expander(f"Total Ads: {len(df)} - ({tomorrow})", expanded=True)
    else:
        df = df_today
        st.markdown(f"### Total Ads: {len(df)}")
        st.markdown(f"#### Date: {today}")
        expander = st.expander(f"Job Details", expanded=True)
    
    expander.dataframe(df[["Occupation", "Employer Name", "Workplace City"]], hide_index=True)
    
    return df

# grouping df with column choice, and showing metrics, removes "Ej Angiven" value from column
def metrics_view(df, column=None):
    df = df[df[column] != "Ej Angiven"]
    df = aggregate_by_group(df, column)
    if column is not None:
        st.markdown(f"## Top 5: {column}s")
        show_metrics(df, column, "Vacancies", 5)

# plot tab used with df from filtering in Analytics-page, plots bar, pie and line charts
def plot_tab(df, column):
    bar, pie, line = st.tabs(["Overview", "Details", "Jobs Over Time"])
    
    # removes unnessecary column values
    df = df[(df[column] != "Ej Angiven") & (df[column] != "Not Specified") & (df[column] != "Undefined")]
    
    line_chart_df = df.groupby(["Publication Date", "Occupation Field"]).size().reset_index(name="Total Ads")
    
    # bar plot with slider to show more or less bars in the chart, based on total vacancies by groped column
    with bar:
        num_groups = st.slider("Number of groups to show", min_value=1, max_value=10, value=5)
        bar_df = aggregate_by_group(df, column)
        st.markdown("### Total vacancies for top " + str(num_groups) + " " + column)
        fig = px.bar(bar_df.head(num_groups), x=column, y="Vacancies", color=column)
        st.plotly_chart(fig)
    
    # pie chart for easy analytics in specific columns
    with pie:
        choice = st.pills("select column:", [f"{column}", "Salary Description", "Duration", "Working Hours Type", "Driver License", "Experience Required"], default=column, label_visibility="hidden")
        st.markdown(f"### Details for {choice} based on total vacancies")
        df = df[(df[choice] != "Ej Angiven") & (df[choice] != "Not Specified") & (df[choice] != "Undefined") & (df[choice] != "Ej specificerad")]
        pie_df = aggregate_by_group(df, choice)
        if pie_df[choice].nunique() > 10:
            fig = px.pie(pie_df.head(10), values="Vacancies", names=choice, color=choice)
        else:
            fig = px.pie(pie_df, values="Vacancies", names=choice, color=choice)
        st.plotly_chart(fig)
    
    # line plot for seeing trends in ammount of job ads and vacancies uploaded to arbetsförmedlingen
    with line:
        st.markdown(f"### Total job ads over time by Occupation Field \n ##### ({df["Publication Date"].min().date()} - {df["Publication Date"].max().date()})")
        fig = px.line(line_chart_df, x="Publication Date", y="Total Ads", color="Occupation Field", line_shape='linear')
        fig.update_layout(
            template="plotly_white",  
            hovermode="x unified",  
            margin=dict(l=20, r=20, t=60, b=40),
            height=500,
        )
        fig.update_xaxes(
            tickformat="%Y-%m-%d",  
            tickangle=45,
            showgrid=True
        )
        st.plotly_chart(fig)

# description tab for filtered df, for getting better understanding of the job, with job description and use of gemini llm for summarization of long descriptions
def desc_tab(df, choice):
    st.markdown("### Job Advertisement Description")
    
    # Selectbox för Headline
    headline = st.selectbox("Matched job ads based on filters",["Select a job ad"] + df["Headline"].unique().tolist())
    job_ad = df[df["Headline"] == headline]
    
    job_ad = job_ad.rename(columns={
        "Employer Workplace": "Employer",
        "Workplace City": "City",
        "Working Hours Type": "Hours"
        })
    if headline != "Select a job ad":
        st.dataframe(job_ad[["Occupation", "Employer", "City", "Duration", "Hours"]], hide_index=True)
    # Annonsbeskrivning för Headline
    if headline == "Select a job ad":
        st.info("Select a job ad to see the description")
    else:
        summarize_description(job_ad)
    