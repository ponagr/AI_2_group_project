from pathlib import Path
import os
import pandas as pd
import duckdb
import streamlit as st
import matplotlib.pyplot
import plotly.express as px

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


# Enkel barplot med val från selectbox
def barplot_df(df, column, bar_ammount = 5):
    return px.bar(df.head(bar_ammount), y="Vacancies", x=column)


# Enkel gruppering till plots och metrics med selectbox val
def group_by(df, column):
    return df.groupby(column)["Vacancies"].sum().reset_index().sort_values("Vacancies", ascending=False)


# Ta bort redan använda kolumner för nästa selectbox
def filter_selectbox(cols, selected):
    for string in cols:
        if string == selected:
            cols.remove(string)
    return cols


# Enkel filtrering av df vid selectbox val
def filter_df(df, column, statement):
    return df[df[column] == statement]


# Sortera kolumner efter antal vacancies till selectboxes
def order_vacancies(df, col):
    return (df.groupby(col)["Vacancies"].sum().sort_values(ascending=False).index.tolist())


def df_overview(df):
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
    antal_heltid = (df["Working Hours Type"] == "Heltid").sum()
    antal_korkort = (df["Driver License"] == True).sum()
    antal_experience = (df["Experience Required"] == True).sum()

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
    # # Metric för totalt antal
    # total_ads = len(df)
    # total_jobs = df["Vacancies"].sum()
    # unique_cities = df["Workplace City"].nunique()
    # unique_occupations = df["Occupation"].nunique()
    # unique_employers = df["Employer Name"].nunique()
    
    # st.markdown("## Översikt")
    # values1 = [total_ads,total_jobs, unique_cities, unique_occupations, unique_employers]
    # labels1 = ["Antal unika job ads","Antal lediga jobb","Antal orter","Unika yrken","Arbetsgivare"]
    # metrics(values1, labels1, 5)
    
    # # Metric för andel i %
    # antal_heltid = (df["Working Hours Type"] == "Heltid").sum()
    # antal_korkort = (df["Driver License"] == True).sum()
    # antal_experience = (df["Experience Required"] == True).sum()

    # heltid_andel = round(antal_heltid / total_jobs * 100, 1)
    # korkort_andel = round(antal_korkort / total_jobs * 100, 1)
    # experience_andel = round(antal_experience / total_jobs * 100, 1)
    
    # st.markdown("### Krav för jobb")
    # labels2 = ["Heltid", "Körkort", "Tidigare Erfarenhet"]
    # values2 = [f"{heltid_andel}%", f"{korkort_andel} %", f"{experience_andel} %"]
    # metrics(values2, labels2, 3)


def filtered_overview(df):
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
    antal_heltid = (df["Working Hours Type"] == "Heltid").sum()
    antal_korkort = (df["Driver License"] == True).sum()
    antal_experience = (df["Experience Required"] == True).sum()

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

# Hämta df från warehouse
def get_dataframe(query):
    working_directory = Path(__file__).parents[1]
    os.chdir(working_directory)
    
    with duckdb.connect("job_ads_data_warehouse.duckdb") as con:
        df = con.execute(f"SELECT * FROM {query}").df()
    df.columns = df.columns.str.replace("_", " ").str.title()
    return df


# pie charts?
# fixa med license och separera på "," och visa bara unika värden, så man kan hämta ut bara unika till filtrering?
# tabs för filtrering, plots/metrics och en för llm?
def filter_tab(df):
    # Overview
    
    # 2 tabs för fönstret, visa pie chart och metrics till höger om filtreringen
    # with st.expander("Översikt (alla jobb i vyn)", expanded=True):
    #     df_overview(df)
    cols = st.columns(2)
        # Filtrering
    # with cols[0]:
    # with st.expander("Översikt (alla jobb i vyn)", expanded=True):
    #     df_overview(df)   
    with cols[0]:
        select_cols = st.columns(3)
        
        with select_cols[0]:
            # Yrkesområde
            group = st.selectbox("Välj yrkesområde:", ["Alla"] + order_vacancies(df,"Occupation Group"))
            if group != "Alla":
                df = df[df["Occupation Group"] == group]
        with select_cols[1]:
            # Stad
            cities = st.multiselect("Filtrera efter stad(er):", order_vacancies(df,"Workplace City"))
            if cities:
                df = df[df["Workplace City"].isin(cities)]
        with select_cols[2]:
            # Arbetsgivare
            employers = st.multiselect("Filtrera efter arbetsgivare:", order_vacancies(df,"Employer Name"))
            if employers:
                df = df[df["Employer Name"].isin(employers)]

        # Körkort & erfarenhet
        # Lägga till checkbox för inget körkort och ingen erfarenhet där man filtrerar efter == False istället
        top_col = st.columns(2)
        bottom_col = st.columns(2)
        
        # for col in license_col:
        with top_col[0]:
            lic = st.selectbox("Kräver körkort", ["Visa Alla", "Ja", "Nej"])
        with top_col[1]:
            exp = st.selectbox("Kräver erfarenhet", ["Visa Alla", "Ja", "Nej"])
        if lic == "Ja":#st.checkbox("Kräver körkort"):
            df = df[df["Driver License"] == True]
            with bottom_col[0]:
                license = st.multiselect("Filtrera efter körkortstyp:", order_vacancies(df,"Required License"))
            if license:    
                df = df[df["Required License"].isin(license)]
        if lic == "Nej":#st.checkbox("Kräver körkort"):
            df = df[df["Driver License"] == False]
            
        if exp == "Ja":#st.checkbox("Kräver tidigare erfarenhet"):
            df = df[df["Experience Required"] == True]
            with bottom_col[1]:
                experience = st.multiselect("Filtrera efter skills:", order_vacancies(df,"Required Skills"))
            if experience:
                df = df[df["Required Skills"].isin(experience)]
        if exp == "Nej":
            df = df[df["Experience Required"] == False]
            
    with cols[1]:        
        with st.expander("Översikt (filtrerad)", expanded=True):
            filtered_overview(df)
    # with st.expander("Översikt (filtrerad)", expanded=True):
    #     filtered_overview(df)
    return df
    # else:
    #     st.warning("Ingen data matchar dina val. Justera filtren för att se resultat.")


def plot_tab(df):
    # dela upp i 2 columns, en för filtrering och metrics, en med plot
    # if not df.empty:
    # with st.expander("Översikt (filtrerad)", expanded=True):
    #     filtered_overview(df)
    cols = st.columns(2)
    
    with cols[0]:
    # Göra till en annan tab, med plots och metrics, och en för 
    # Metrics och Barcharts
        main_columns = ["Occupation Group", "Employer Name", "Occupation", "Workplace City"]
        choice = st.selectbox("Välj kolumn att gruppera på:", main_columns)

        st.markdown(f"## Topp 5: {choice}")
        new_df = group_by(df, choice)
        show_metrics(new_df, choice, "Vacancies", 5)

        rows = st.selectbox("Välj specifikt värde:", ["Visa alla"] + order_vacancies(df,choice))
        max_bars = 15
        if len(new_df) < max_bars:
            max_bars = len(new_df)
        bars = st.slider("Antal staplar att visa:", min_value=5, max_value=max_bars, step=1, key=f"{choice}")
        
    with cols[1]:
        with st.expander("Översikt (filtrerad)", expanded=True):
            filtered_overview(df)
            
    if rows == "Visa alla":
        st.plotly_chart(barplot_df(new_df, choice, bars))
    else:
        filtered_df = filter_df(df, choice, rows)
        st.plotly_chart(barplot_df(group_by(filtered_df, "Headline"), "Headline", bars))
        return filtered_df
    return df
    # else:
    #     st.warning("Ingen data matchar dina val. Justera filtren för att se resultat.")


def desc_tab(df):
    # if not df.empty:
            # Selectbox för Headline
    cols = st.columns(2)
    with cols[0]:
        st.markdown("### Jobbannonsbeskrivning")
        headline = st.selectbox("Matchade jobbannonser baserad på filtrering:",["Välj jobbannons"] + df["Headline"].unique().tolist())
        job_ad = df[df["Headline"] == headline]
    # Annonsbeskrivning för Headline
        if headline == "Välj jobbannons":
            st.info("Välj en jobbannons för beskrivning")
        else:
            st.dataframe(job_ad[["Headline", "Employer Name", "Employer Workplace", "Employer Organization Number", "Workplace City", "Duration", "Working Hours Type"]])
            st.info(job_ad[job_ad["Description"].notnull()].iloc[0]["Description"])
    with cols[1]:
        with st.expander("Översikt (filtrerad)", expanded=True):
            filtered_overview(df)
    # else:
    #     st.warning("Ingen data matchar dina val. Justera filtren för att se resultat.")

# line plot för trender mellan 2 datum, bar plot för att visa månader med flest nya jobb, filtrera och visa olika trender
# dela upp selectboxes i flera cols

def layout():
    # Vyer för olika marts
    page = {
        "Alla jobb": "mart.mart_full_job_ads", 
        "Transport, Distribution, Lager": "mart.mart_transport_distrubution_layer",
        "Installation, Drift, Underhåll": "mart.mart_installation_maintenence",
        "Hotell, Restaurang, Storhushåll": "mart.mart_hotel_restaurant"
    }

    # Hämta df baserat på val av vy
    view_choice = st.sidebar.radio("Välj vy", list(page.keys()))
    df = get_dataframe(page[view_choice])

    st.markdown(f"# Jobbdata för: {view_choice}")
    with st.expander("Översikt (alla jobb i vyn)", expanded=True):
        df_overview(df)   
    
    tabs_dict = {
        "Filtrering": filter_tab,
        "Plots/Metrics": plot_tab,
        "Job Description/LLM": desc_tab
    }
    tabs = st.tabs(tabs_dict.keys())
    
    for tab, func in zip(tabs, tabs_dict.values()):
        with tab:
            if not df.empty:
                df = func(df)
            else:
                st.warning("Ingen data matchar dina val. Justera filtren för att se resultat.")
        # # Overview
        # with st.expander("Översikt (alla jobb i vyn)", expanded=True):
        #     df_overview(df)

        # # Filtrering
        
        # # Yrkesområde
        # group = st.selectbox("Välj yrkesområde:", ["Alla"] + order_vacancies(df,"Occupation Group"))
        # if group != "Alla":
        #     df = df[df["Occupation Group"] == group]

        # # Stad
        # cities = st.multiselect("Filtrera efter stad(er):", order_vacancies(df,"Workplace City"))
        # if cities:
        #     df = df[df["Workplace City"].isin(cities)]

        # # Arbetsgivare
        # employers = st.multiselect("Filtrera efter arbetsgivare:", order_vacancies(df,"Employer Name"))
        # if employers:
        #     df = df[df["Employer Name"].isin(employers)]

        # # Körkort & erfarenhet
        # # Lägga till checkbox för inget körkort och ingen erfarenhet där man filtrerar efter == False istället
        # if st.checkbox("Kräver körkort"):
        #     df = df[df["Driver License"] == True]
        #     license = st.multiselect("Filtrera efter körkortstyp:", order_vacancies(df,"Required License"))
        #     if license:    
        #         df = df[df["Required License"].isin(license)]
        # if st.checkbox("Kräver tidigare erfarenhet"):
        #     df = df[df["Experience Required"] == True]
        #     experience = st.multiselect("Filtrera efter skills:", order_vacancies(df,"Required Skills"))
        #     if experience:
        #         df = df[df["Required Skills"].isin(experience)]

    # st.markdown("---")
    
    # with st.expander("Översikt (filtrerad)", expanded=True):
    #     filtered_overview(df)
    # # Göra till en annan tab, med plots och metrics, och en för 
    # # Metrics och Barcharts
    # main_columns = ["Occupation Group", "Employer Name", "Occupation", "Workplace City"]
    # choice = st.selectbox("Välj kolumn att gruppera på:", main_columns)

    # if not df.empty:
    #     st.markdown(f"## Topp 5: {choice}")
    #     new_df = group_by(df, choice)
    #     show_metrics(new_df, choice, "Vacancies", 5)

    #     rows = st.selectbox("Välj specifikt värde:", ["Visa alla"] + order_vacancies(df,choice))
    #     max_bars = 15
    #     if len(new_df) < max_bars:
    #         max_bars = len(new_df)
    #     bars = st.slider("Antal staplar att visa:", min_value=5, max_value=max_bars, step=1, key=f"{choice}")

    #     # Selectbox för Headline
    #     if rows == "Visa alla":
    #         st.plotly_chart(barplot_df(new_df, choice, bars))
    #         headline = st.selectbox("Matchade jobbannonser baserad på filtrering:",["Välj jobbannons"] + df["Headline"].unique().tolist())
    #         job_ad = df[df["Headline"] == headline]
    #     else:
    #         filtered_df = filter_df(df, choice, rows)
    #         st.plotly_chart(barplot_df(group_by(filtered_df, "Headline"), "Headline", bars))
    #         headline = st.selectbox("Matchade jobbannonser baserad på filtrering:",["Välj jobbannons"] + filtered_df["Headline"].unique().tolist())
    #         job_ad = filtered_df[filtered_df["Headline"] == headline]
        
        
    #     # Annonsbeskrivning för Headline
    #     st.markdown("### Jobbannonsbeskrivning")
    #     if headline == "Välj jobbannons":
    #         st.info("Välj en jobbannons för beskrivning")
    #     else:
    #         st.info(job_ad[job_ad["Description"].notnull()].iloc[0]["Description"])
    # else:
    #     st.warning("Ingen data matchar dina val. Justera filtren för att se resultat.")


if __name__ == "__main__":
    layout()
