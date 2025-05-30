import streamlit as st
from components.sidebar import render_sidebar
from gemini.llm import summarize_occupation_group, skills_per_occupation_group

st.set_page_config(page_title="Summary llm", layout="wide")

df, field = render_sidebar()

st.title("Summary llm")

selected = st.selectbox("Select occupation group", sorted(df["Occupation Group"].unique()))
df = df[df["Occupation Group"] == selected]

if len(df) < 10:
    st.warning("Too few job ads in this occupation group to provide a meaningful summary.")
else:
    col1, col2 = st.columns(2)
    with col1:
        with st.spinner("Awaiting response.."):
            summarize_occupation_group(df)
    with col2:
        with st.spinner("Awaiting response.."):
            skills_per_occupation_group(df)