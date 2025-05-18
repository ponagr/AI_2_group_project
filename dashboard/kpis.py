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

# Enkel filtrering av df vid selectbox val
def filter_df(df, column, statement):
    return df[df[column] == statement]

# Enkel gruppering till plots och metrics med selectbox val
def group_by(df, column):
    return df.groupby(column)["Vacancies"].sum().reset_index().sort_values("Vacancies", ascending=False)

def overview(df):
    # Metric för totalt antal
    total_ads = len(df)
    total_jobs = df["Vacancies"].sum()
    unique_groups = df["Occupation Group"].nunique()
    unique_cities = df["Workplace City"].nunique()
    unique_occupations = df["Occupation"].nunique()
    unique_employers = df["Employer Name"].nunique()
    
    st.markdown("### Totalt antal")
    values = [total_ads, total_jobs]
    labels = ["Job ads","Lediga jobb"]
    metrics(values, labels, 2)
    
    # Metric för andel i %
    antal_heltid = df[df["Working Hours Type"] == "Heltid"]["Vacancies"].sum()
    antal_korkort = df[df["Driver License"] == True]["Vacancies"].sum()
    antal_experience = df[df["Experience Required"] == True]["Vacancies"].sum()

    heltid_andel = round(antal_heltid / total_jobs * 100, 1)
    korkort_andel = round(antal_korkort / total_jobs * 100, 1)
    experience_andel = round(antal_experience / total_jobs * 100, 1)
    
    st.markdown("### Krav för jobb")
    labels2 = ["Heltid", "Körkort", "Tidigare Erfarenhet"]
    values2 = [f"{heltid_andel}%", f"{korkort_andel} %", f"{experience_andel} %"]
    metrics(values2, labels2, 3)

    st.markdown("### Unikt antal")
    values1 = [unique_groups, unique_employers, unique_occupations, unique_cities]
    labels1 = ["Yrkesgrupper","Arbetsgivare","Yrken","Orter"]
    metrics(values1, labels1, 4)