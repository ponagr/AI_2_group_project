from pathlib import Path
import os
import pandas as pd
import duckdb

# Hämta df från warehouse
def get_dataframe(query):
    working_directory = Path(__file__).parents[1]
    os.chdir(working_directory)
    
    with duckdb.connect("job_ads_data_warehouse.duckdb") as con:
        df = con.execute(f"SELECT * FROM {query}").df()
    df.columns = df.columns.str.replace("_", " ").str.title()
    return df