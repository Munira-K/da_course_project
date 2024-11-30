import streamlit as st
import pandas as pd
# import plotly.express as px
from etl import fetch_data_from_view

#Создает заголовок страничке
st.title('Таблицы базы :blue-background[телеком-услуг] :book:')

#Показывает таблицу customers и ее краткое описание на странице с таблицами
customers = fetch_data_from_view('customers2')
st.header("Таблица: customers")
if st.checkbox('Показать/скрыть данные таблицы : customers'):
    st.write("Таблица содержит информацию о клиентах, включая уникальный идентификатор клиента (customerID), пол, статус пенсионера, информацию о партнерах")
    st.dataframe(customers)
    
#Показывает таблицу services и ее краткое описание на странице с таблицами
services = fetch_data_from_view('services2')
st.header("Таблица: services")
if st.checkbox('Показать/скрыть данные таблицы :services'):
    st.write('Эта таблица хранит информацию о сервисах, которые использует клиент ')
    st.dataframe(services)

#Показывает таблицу contracts и ее краткое описание на странице с таблицами
contracts = fetch_data_from_view('contracts2')
st.header("Таблица: contracts")
if st.checkbox('Показать/скрыть данные таблицы : contracts'):
    st.write('Включает информацию о контрактах клиентов, таких как тип контракта, методы оплаты, даты начала и окончания контракта.')
    st.dataframe(contracts)

#Показывает таблицу financials и ее краткое описание на странице с таблицами
financials = fetch_data_from_view('financials2')
st.header("Таблица: financials")
if st.checkbox('Показать/скрыть данные таблицы : financials'):
    st.write('Содержит финансовые данные о клиентах, включая ежемесячные и общие платежи, отток клиентов (churn) и дату последнего платежа.')
    st.dataframe(financials)

#Показывает таблицу payment_methods и ее краткое описание на странице с таблицами
payment_methods = fetch_data_from_view('payment_methods2')
st.header("Таблица: payment_methods")
if st.checkbox('Показать/скрыть данные таблицы:payment_methods'):
    st.write('Хранит информацию о методах оплаты')
    st.dataframe(payment_methods)





