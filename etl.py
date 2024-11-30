import duckdb
import pandas as pd

def fetch_data_from_view(view_name, database_path='my.db'):
    """
    Извлекает данные из вьюшки с бд и возвращает их в виде DataFrame.Работает следующим образом:
        - Создаёт соединение с базой данных.
        - Извлекает все данных из указанной вьюшки.
        - Закрывает соединение и возвращает результат в виде DataFrame.
    """
    query = f"SELECT * FROM {view_name};"
    con = duckdb.connect(database=database_path)
    df = con.execute(query).fetchdf()
    con.close()
    return df
