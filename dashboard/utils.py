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