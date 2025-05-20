import streamlit as st

def filter_tab(df):
    # Initiate min and max date
    min_date = df["Publication Date"].min().date()
    max_date = df["Publication Date"].max().date()
    start_date = min_date
    end_date = max_date
    
    with st.expander("Filter"):
        cols = st.columns(2)
        
        # Yrkesområde
        group = cols[0].selectbox("Välj yrkesområde:", ["Alla"] + order_vacancies(df,"Occupation Group"))
        if group != "Alla":
            df = df[df["Occupation Group"] == group]
        
        # Stad
        cities = cols[0].multiselect("Filtrera efter stad(er):", order_vacancies(df,"Workplace City"))
        if cities:
            df = df[df["Workplace City"].isin(cities)]
        
        # Arbetsgivare
        employers = cols[0].multiselect("Filtrera efter arbetsgivare:", order_vacancies(df,"Employer Name"))
        if employers:
            df = df[df["Employer Name"].isin(employers)]

        # Publiceringsdatum
        with cols[1]:
            col1, col2 = st.columns(2)
            
            start_date = pd.to_datetime(col1.date_input("Start date", min_value=min_date, max_value=max_date, value=start_date))
            end_date = pd.to_datetime(col2.date_input("End date", min_value=min_date, max_value=max_date, value=end_date))
            
            if end_date < start_date:
                end_date = start_date
            
            df = df[(df["Publication Date"] <= end_date) & (df["Publication Date"] >= start_date)]
        
        # Körkort & erfarenhet
            lic = col1.selectbox("Kräver körkort", ["Visa Alla", "Ja", "Nej"])
            exp = col2.selectbox("Kräver erfarenhet", ["Visa Alla", "Ja", "Nej"])
            
            if lic == "Ja":
                df = df[df["Driver License"] == True]
                
                # Splitta på listor och skriv ut unika värden till selectbox
                license = col1.multiselect("Filtrera efter körkortstyp:", split_unique_cols(df,"Required License"))
                if license:   
                    # Hitta matchningar, där värdet från select finns nånstans i kolumnens värde separerat av ','
                    df = df[df["Required License"].fillna("").apply(lambda x: any(lic in [s.strip() for s in x.split(',')] for lic in license))]
            if lic == "Nej":
                df = df[df["Driver License"] == False]
            
            if exp == "Ja":
                df = df[df["Experience Required"] == True]
                with col2:
                    # Splitta på listor och skriv ut unika värden till selectbox
                    experience = st.multiselect("Filtrera efter skills:", split_unique_cols(df,"Required Skills"))
                if experience:
                    # Hitta matchningar, där värdet från select finns nånstans i kolumnens värde separerat av ','
                    df = df[df["Required Skills"].fillna("").apply(lambda x: any(exp in [e.strip() for e in x.split(',')] for exp in experience))]
            if exp == "Nej":
                df = df[df["Experience Required"] == False]
                
        # Arbetstid
        work_time = cols[0].pills("Heltid/Deltid", ["Visa Alla", "Heltid", "Deltid"], selection_mode='single', default="Visa Alla")
        if work_time != "Visa Alla":
            df = df[df["Working Hours Type"] == work_time]
    
    return df