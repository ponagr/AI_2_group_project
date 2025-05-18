import pandas as pd
import streamlit as st
from plots import barplot_df
from read_data import get_dataframe
from kpis import show_metrics, filter_df, group_by, overview


# Ta bort redan använda kolumner för nästa selectbox
def filter_selectbox(cols, selected):
    for string in cols:
        if string == selected:
            cols.remove(string)
    return cols


# Sortera kolumner efter antal vacancies till selectboxes
def order_vacancies(df, col):
    return (df.groupby(col)["Vacancies"].sum().sort_values(ascending=False).index.tolist())


def split_unique_cols(df, column):
    split_cols = df[column].dropna().str.split(",")
    strip_cols = [col.strip() for strip_list in split_cols for col in strip_list]
    return sorted(set(strip_cols))




# pie charts?
# fixa med license och separera på "," och visa bara unika värden, så man kan hämta ut bara unika till filtrering?
# tabs för filtrering, plots/metrics och en för llm?

def filter_tab(df):
    # Overview
    
    # 2 tabs för fönstret, visa pie chart och metrics till höger om filtreringen
    cols = st.columns(2)
    # Filtrering
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
        
        with top_col[0]:
            lic = st.selectbox("Kräver körkort", ["Visa Alla", "Ja", "Nej"])
        with top_col[1]:
            exp = st.selectbox("Kräver erfarenhet", ["Visa Alla", "Ja", "Nej"])
        if lic == "Ja":
            df = df[df["Driver License"] == True]
            with bottom_col[0]:
                # Splitta på listor och skriv ut unika värden till selectbox
                license = st.multiselect("Filtrera efter körkortstyp:", split_unique_cols(df,"Required License"))
            if license:   
                # Hitta matchningar, där värdet från select finns nånstans i kolumnens värde separerat av ','
                df = df[df["Required License"].fillna("").apply(lambda x: any(lic in [s.strip() for s in x.split(',')] for lic in license))]
        if lic == "Nej":
            df = df[df["Driver License"] == False]
            
        if exp == "Ja":
            df = df[df["Experience Required"] == True]
            with bottom_col[1]:
                # Splitta på listor och skriv ut unika värden till selectbox
                experience = st.multiselect("Filtrera efter skills:", split_unique_cols(df,"Required Skills"))
            if experience:
                # Hitta matchningar, där värdet från select finns nånstans i kolumnens värde separerat av ','
                df = df[df["Required Skills"].fillna("").apply(lambda x: any(exp in [e.strip() for e in x.split(',')] for exp in experience))]
        if exp == "Nej":
            df = df[df["Experience Required"] == False]
            
    with cols[1]:        
        with st.expander("Översikt (filtrerad)", expanded=True):
            overview(df)
    return df



def plot_tab(df):
    # dela upp i 2 columns, en för filtrering och metrics, en med plot
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
            overview(df)
            
    if rows == "Visa alla":
        st.plotly_chart(barplot_df(new_df, choice, bars))
    else:
        filtered_df = filter_df(df, choice, rows)
        st.plotly_chart(barplot_df(group_by(filtered_df, "Headline"), "Headline", bars))
        return filtered_df
    return df


def desc_tab(df):
    cols = st.columns(2)
    with cols[0]:
        st.markdown("### Jobbannonsbeskrivning")
        
        # Selectbox för Headline
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
            overview(df)


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
        overview(df)   
    
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



if __name__ == "__main__":
    layout()
