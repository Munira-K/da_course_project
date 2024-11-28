import streamlit as st
import pandas as pd
# import plotly.express as px
# from etl import fetch_data_from_view

st.title('Таблицы базы :blue-background[телеком-услуг] :book:')

customers = fetch_data_from_view('customers2')
st.header("Таблица: customers")
if st.checkbox('Показать/скрыть данные таблицы : customers'):
    st.write("Таблица содержит информацию о клиентах, включая уникальный идентификатор клиента (customerID), пол, статус пенсионера, информацию о партнерах")
    st.dataframe(customers)
    

services = fetch_data_from_view('services2')
st.header("Таблица: services")
if st.checkbox('Показать/скрыть данные таблицы :services'):
    st.write('Эта таблица хранит информацию о сервисах, которые использует клиент ')
    st.dataframe(services)

contracts = fetch_data_from_view('contracts2')
st.header("Таблица: contracts")
if st.checkbox('Показать/скрыть данные таблицы : contracts'):
    st.write('Включает информацию о контрактах клиентов, таких как тип контракта, методы оплаты, даты начала и окончания контракта.')
    st.dataframe(contracts)

financials = fetch_data_from_view('financials2')
st.header("Таблица: financials")
if st.checkbox('Показать/скрыть данные таблицы : financials'):
    st.write('Содержит финансовые данные о клиентах, включая ежемесячные и общие платежи, отток клиентов (churn) и дату последнего платежа.')
    st.dataframe(financials)

payment_methods = fetch_data_from_view('payment_methods2')
st.header("Таблица: payment_methods")
if st.checkbox('Показать/скрыть данные таблицы:payment_methods'):
    st.write('Хранит информацию о методах оплаты')
    st.dataframe(payment_methods)





