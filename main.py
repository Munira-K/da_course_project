import streamlit as st
import pandas as pd
# import plotly.express as px
# from etl import fetch_data_from_view

# Создает главную страницу с разделениями по Таблицам и Кратким анализом
pages = [
    st.Page('tables.py', title = 'Таблицы'),
    st.Page('dashboards.py', title = 'Краткий анализ')
]

pg = st.navigation(pages)
pg.run()
