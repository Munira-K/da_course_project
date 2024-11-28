import duckdb
import pandas as pd

def fetch_data_from_view(view_name, database_path='my.db'):

    query = f"SELECT * FROM {view_name};"
    con = duckdb.connect(database=database_path)
    df = con.execute(query).fetchdf()
    con.close()
    return df
