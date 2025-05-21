import streamlit as st
import pandas as pd

# Metrics med hjälp av df och kolumner
def show_metrics(df:pd.DataFrame, metric_labels:str, metric_kpis:str, metric_amount:int):
    """Function for generating metrics 

    Args:
        df (dataframe): dataframe to filter metrics from
        metric_labels (str): string for metric labels using df["metric_labels"] to filter out label values from df
        metric_kpis (str): string for metric kpis using df["metric_kpis"] to filter out kpi values from df
        metric_amount (int): integer for amount of metric columns to use
    """
    labels = df[metric_labels].head(metric_amount)
    cols = st.columns(metric_amount)
    kpis = df[metric_kpis].head(metric_amount)

    for col, label, kpi in zip(cols, labels, kpis):
        with col: 
            st.metric(label=label, value=kpi)


# Simpel metric för att kunna återanvända variabelnamn och korta ner kod
def metrics(kpis,labels,col_amount):
    cols = st.columns(col_amount)
    for col, label, kpi in zip(cols, labels, kpis):
        with col: 
            st.metric(label=label, value=kpi)

def sidebar_metrics(kpis,labels,col_amount):
    cols = st.sidebar.columns(col_amount)
    for col, label, kpi in zip(cols, labels, kpis):
        with col: 
            st.sidebar.metric(label=label, value=kpi)


def overview(df):
    # Metric för totalt antal
    total_ads = len(df)
    total_jobs = df["Vacancies"].sum()
    unique_groups = df["Occupation Group"].nunique()
    unique_cities = df["Workplace City"].nunique()
    unique_occupations = df["Occupation"].nunique()
    unique_employers = df["Employer Workplace"].nunique()
    
    values = [total_ads, total_jobs]
    col1, col2= st.columns(2)
    col1.metric("Job ads", total_ads)
    col2.metric("Vacancies", total_jobs)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Occupation Groups", unique_groups)
    col2.metric("Employers", unique_employers)
    col3.metric("Occupations", unique_occupations)
    col4.metric("Cities", unique_cities)
    # labels = ["Job ads","Lediga jobb"]
    # metrics(values, labels, 2)
    
    # values1 = [unique_groups, unique_employers, unique_occupations, unique_cities]
    # labels1 = ["Yrkesgrupper","Arbetsgivare","Yrken","Orter"]
    # metrics(values1, labels1, 4)