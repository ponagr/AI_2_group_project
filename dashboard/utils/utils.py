from pathlib import Path
import streamlit as st
import duckdb

def load_data(query):
    db_path = Path(__file__).parents[1] / "job_ads_data_warehouse.duckdb"
    with duckdb.connect(str(db_path)) as con:
        df = con.execute(f"SELECT * FROM {query}").df()
    df.columns = df.columns.str.replace("_", " ").str.title()
    return df

def get_df():
    if "df" in st.session_state:
        return st.session_state["df"]
    else:
        st.warning("Dataframe not found in session state.")
        st.stop()

# Sortera kolumner efter antal vacancies till selectboxes
def group_and_sort(df, group_col, agg_col="Vacancies", agg="sum"):
    # Grouping the data by the group_col and aggregating the agg_col
    if agg == "sum":
        grouped_df = df.groupby(group_col)[agg_col].sum().reset_index()
    elif agg == "count":
        grouped_df = df.groupby(group_col)[agg_col].count().reset_index()
    else:
        raise ValueError("agg must be either sum or count")
    
    sorted_df = grouped_df.sort_values(by=agg_col, ascending=False)
    
    return sorted_df

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