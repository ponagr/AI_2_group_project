from pathlib import Path
import streamlit as st
import duckdb

# function to load and return dataframe from data warehouse based on choice (query) in dashboard
def load_data(query):
    db_path = Path(__file__).parents[2] / "job_ads_data_warehouse.duckdb"
    with duckdb.connect(str(db_path)) as con:
        df = con.execute(f"SELECT * FROM {query}").df()
    # changes column names for cleaner text in dashboard
    df.columns = df.columns.str.replace("_", " ").str.title()
    return df

def get_df():
    if "df" in st.session_state:
        return st.session_state["df"]
    else:
        st.warning("Dataframe not found in session state.")
        st.stop()

# Sortera kolumner efter antal vacancies till selectboxes
def get_sorted_group_labels(df, group_col, agg_col="Vacancies", agg="sum"):
    # Grouping the data by the group_col and aggregating the agg_col
    if agg == "sum":
        grouped_df = df.groupby(group_col)[agg_col].sum()
    elif agg == "count":
        grouped_df = df.groupby(group_col)[agg_col].count()
    else:
        raise ValueError("agg must be either sum or count")
    
    sorted_df = grouped_df.sort_values(ascending=False).index.tolist()
    
    return sorted_df

# groups dataframe column with total vacancies, used for plotting and metrics
def aggregate_by_group(df, group_col, agg_col="Vacancies"):
    return df.groupby(group_col)[agg_col].sum().reset_index().sort_values(agg_col, ascending=False)

def split_unique_cols(df, column):
    split_cols = df[column].dropna().str.split(",")
    strip_cols = [col.strip() for strip_list in split_cols for col in strip_list]
    return sorted(set(strip_cols))

# Ta bort redan använda kolumner för nästa selectbox
def filter_selectbox(cols, selected):
    for string in cols:
        if string == selected:
            cols.remove(string)
    return cols

# filters df
def filter_df(df, column, statement):
    return df[df[column] == statement]