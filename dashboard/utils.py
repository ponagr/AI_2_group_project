import duckdb

def load_data(query):
    with duckdb.connect(database='../job_ads_data_warehouse.duckdb', read_only=True) as con:
        return con.execute(query).fetch_df()