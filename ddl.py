import duckdb
import pandas as pd
import os


def create_tables(database_path='my.db', tables_sql_path='queries/create_tables.sql'):
    """
    Создаёт таблицы в базе данных. Работает следующим образом:
        - Удаляет таблицы, если они уже существуют.
        - Читает SQL-запросы из файла и создаёт новые таблицы.
    """
    con = duckdb.connect(database=database_path)
    con.execute("DROP TABLE IF EXISTS services;")
    con.execute("DROP TABLE IF EXISTS contracts;")
    con.execute("DROP TABLE IF EXISTS financials;")
    con.execute("DROP TABLE IF EXISTS payment_methods;")
    con.execute("DROP TABLE IF EXISTS customers;")
    
    with open(tables_sql_path, 'r', encoding='utf-8') as f:
        create_tables_sql = f.read()
    con.execute(create_tables_sql)
    con.close()

def load_data(database_path='my.db', source_folder='source'):
    """
    Загружает данные из Excel-файлов в таблицы базы данных.Работает следующим образом:
        - Для каждой таблицы загружает данные из соответствующего листа Excel-файла.
        - Удаляет существующие записи в таблицах перед загрузкой новых данных.
        - Возвращает результат загрузки для каждой таблицы.
    """
    con = duckdb.connect(database=database_path)
    data_files = {
        'customers': 'customers',
        'services': 'services',
        'contracts': 'contracts',
        'financials': 'financials',
        'payment_methods': 'payment_methods'
    }

    for table_name, sheet_name in data_files.items():
        file_path = os.path.join(source_folder, 'telecom_users.xlsx')
        if os.path.exists(file_path):
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            con.execute(f"DELETE FROM {table_name};")
            try:
                con.execute(f"INSERT INTO {table_name} SELECT * FROM df;")
                print(f"Данные загружены в таблицу '{table_name}' из листа '{sheet_name}'.")
            except Exception as e:
                print(f"Ошибка при загрузке данных в таблицу '{table_name}': {e}")
                con.close()
                return
        else:
            print(f"Файл '{file_path}' не найден.")
    con.close()


def create_views(database_path='my.db', views_sql_path='queries/create_views.sql'):
    """
    Создаёт вьюшки в базе данных на основе SQL-запросов.Работает следующим образом:
        - Читает SQL-запросы из файла.
        - Создаёт представления в базе данных.
    """
    con = duckdb.connect(database=database_path)
    with open(views_sql_path, 'r') as f:
        create_views_sql = f.read()
    con.execute(create_views_sql)
    con.close()


if __name__ == '__main__':
#Cозданиe, загрузка таблиц и представлений , отслеживание статуса процессоа
    print("Создание таблиц...")
    create_tables()
    print("Таблицы успешно созданы.")

    print("Загрузка данных в таблицы...")
    load_data()
    print("Данные успешно загружены.")

    print("Создание представлений...")
    create_views()
    print("Представления успешно созданы.")
