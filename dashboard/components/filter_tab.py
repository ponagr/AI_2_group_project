import streamlit as st
import pandas as pd
from utils.utils import split_unique_cols
from components.kpis import overview

def filter_tab(df):
    # Initiate min and max date
    min_date = df["Publication Date"].min().date()
    max_date = df["Publication Date"].max().date()
    start_date = min_date
    end_date = max_date
    filtered_df = df.copy()
    
    with st.expander("Filter"):
        cols = st.columns(2)
        
        # Yrkesområde
        group = cols[0].selectbox("Välj yrkesområde:", ["Alla"] + sorted(filtered_df["Occupation Group"].unique()))
        if group != "Alla":
            filtered_df = filtered_df[filtered_df["Occupation Group"] == group]
        
        # Stad
        cities = cols[0].multiselect("Filtrera efter stad(er):", sorted(filtered_df["Workplace City"].unique()))
        if cities:
            filtered_df = filtered_df[filtered_df["Workplace City"].isin(cities)]
        
        # Arbetsgivare
        employers = cols[0].multiselect("Filtrera efter arbetsgivare:", sorted(filtered_df["Employer Workplace"].unique()))
        if employers:
            filtered_df = filtered_df[filtered_df["Employer Workplace"].isin(employers)]

        # Publiceringsdatum
        with cols[1]:
            col1, col2 = st.columns(2)
            
            start_date = pd.to_datetime(col1.date_input("Start date", min_value=min_date, max_value=max_date, value=start_date))
            end_date = pd.to_datetime(col2.date_input("End date", min_value=min_date, max_value=max_date, value=end_date))
            
            if end_date < start_date:
                end_date = start_date
            
            filtered_df = filtered_df[(filtered_df["Publication Date"] <= end_date) & (filtered_df["Publication Date"] >= start_date)]
        
        # Körkort & erfarenhet
            lic = col1.selectbox("Kräver körkort", ["Visa Alla", "Ja", "Nej"])
            exp = col2.selectbox("Kräver erfarenhet", ["Visa Alla", "Ja", "Nej"])
            
            if lic == "Ja":
                filtered_df = filtered_df[filtered_df["Driver License"] == True]
                
                # Splitta på listor och skriv ut unika värden till selectbox
                license = col1.multiselect("Filtrera efter körkortstyp:", split_unique_cols(filtered_df,"Required License"))
                if license:   
                    # Hitta matchningar, där värdet från select finns nånstans i kolumnens värde separerat av ','
                    filtered_df = filtered_df[filtered_df["Required License"].fillna("").apply(lambda x: any(lic in [s.strip() for s in x.split(',')] for lic in license))]
            if lic == "Nej":
                filtered_df = filtered_df[filtered_df["Driver License"] == False]
            
            if exp == "Ja":
                filtered_df = filtered_df[filtered_df["Experience Required"] == True]
                with col2:
                    # Splitta på listor och skriv ut unika värden till selectbox
                    experience = st.multiselect("Filtrera efter skills:", split_unique_cols(filtered_df,"Required Skills"))
                if experience:
                    # Hitta matchningar, där värdet från select finns nånstans i kolumnens värde separerat av ','
                    filtered_df = filtered_df[filtered_df["Required Skills"].fillna("").apply(lambda x: any(exp in [e.strip() for e in x.split(',')] for exp in experience))]
            if exp == "Nej":
                filtered_df = filtered_df[filtered_df["Experience Required"] == False]
                
        # Arbetstid
        work_time = cols[0].pills("Heltid/Deltid", ["Visa Alla", "Heltid", "Deltid"], selection_mode='single', default="Visa Alla")
        if work_time != "Visa Alla":
            filtered_df = filtered_df[filtered_df["Working Hours Type"] == work_time]
    
        if filtered_df.empty:
            st.warning("Filter gave an empty dataframe")
        else:
            overview(filtered_df)
    
    return filtered_df