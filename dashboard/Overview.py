import streamlit as st
from components.sidebar import render_sidebar
from components.dashboard_views import desc_tab, show_ads
from components.plots import plot_df
from utils.utils import aggregate_by_group
from gemini.llm import overview_description

# First page(Home-page) in dashboard, for getting a quick overview of relevant job ads
st.set_page_config(page_title="Overview", layout="wide")

# calling render_sidebar to get chosen df and occupation field
df, field = render_sidebar()
if field == "Alla jobb":
    st.title("Overview")
else:
    st.title(f"Overview for {field}")

# choice to view jobs published today, och jobs that needs to be applied today
choice = st.pills("Filter by:", ["Published today", "Application deadline today"], default="Published today")
tab1, tab2 = st.tabs(["Plots", "Description"])
with tab1:
    # calling show_ads function to see and overview of the job ads for the chosen field
    df_new = show_ads(df, choice)
    
    # plots the returned df for visualization based on choice bellow
    if field == "Alla jobb":
        col = st.pills("select column:", ["Occupation Field", "Occupation Group", "Occupation", "Workplace City", "Employer Workplace", "Salary Description", "Duration", "Working Hours Type", "Driver License", "Experience Required"], default="Occupation Field", label_visibility="hidden")
    else:
        col = st.pills("select column:", ["Occupation Group", "Occupation", "Workplace City", "Employer Workplace", "Salary Description", "Duration", "Working Hours Type", "Driver License", "Experience Required"], default="Occupation Group", label_visibility="hidden")
    plot_df(aggregate_by_group(df_new, col), col)
    expander = st.expander("Gemini summary of filtered job ads", expanded=False)
    with expander:
        with st.spinner("Awaiting response..."):
            st.markdown(overview_description(df_new, choice), unsafe_allow_html=True)

with tab2:
    # gives some descriptions about the job ads based on the df
    desc_tab(df_new, choice)