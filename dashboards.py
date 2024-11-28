import streamlit as st
import pandas as pd
import plotly.express as px
from etl import fetch_data_from_view

st.title('Анализ клиентской базы :blue-background[телеком-услуг] :book:')

# Фильтры
st.sidebar.header("Фильтры")
year_filter = st.sidebar.radio("Выберите год", options=[2021, 2022, 2023]) 
# partner_filter = st.sidebar.radio("Семейное положение клиента", options=["Yes", "No"])
churn_filter = st.sidebar.radio("Отток клиентов (churn)", options=["Все", "Yes", "No"])

about_churn = fetch_data_from_view('about_churn')
# Применение фильтра по churn
if churn_filter == "Yes":
    about_churn = about_churn[about_churn["churn"] == "Yes"]
elif churn_filter == "No":
    about_churn = about_churn[about_churn["churn"] == "No"]
elif churn_filter != "Все":
    about_churn = about_churn[about_churn["churn"] == churn_filter]

# График 1: Распределение клиентов (Пирог)
cust = fetch_data_from_view('about_customers')
# filtered_cust = cust[cust['partner'] == partner_filter]  # Фильтрация по семейному положению
fig1 = px.pie(cust, names='senior_citizen', title="Распределение клиентов по возрасту")
st.plotly_chart(fig1)

# st.write("Этот дашборд отображает ключевые метрики и аналитические данные о клиентах, услугах и доходах.")


# График 2: Средние траты клиентов
aggregated_df = cust.groupby(['partner', 'dependents'])[['monthly_charges', 'total_charges']].mean().reset_index()
df = aggregated_df.rename(columns={'monthly_charges': 'avg_monthly', 'total_charges': 'avg_total'})
fig2 = px.bar(df, x='partner', y='avg_monthly', color='dependents', barmode='group',
              title="Средние траты клиентов по семейному положению", color_continuous_scale = ['lightblue', 'royalblue'])
st.plotly_chart(fig2)

data1 = cust[['customerID', 'tenure', 'device_protection', 'online_security', 'streamingTV', 'internet_service', 'contract','total_monthly_charges']]\
        .head(10)\
        .sort_values(by=['total_monthly_charges','tenure'], ascending=False)

st.write("**Топ 10 клиентов с наибольшей общей суммой ежемесячных платежей и проведенных месяцев**")
if st.checkbox('Показать/скрыть таблицу'):
    st.dataframe(data1)

# График 3: Использование услуг
about_services = fetch_data_from_view('about_services')
df = about_services[['phone_service', 'multiple_lines', 'online_security', 'online_backup',
                     'device_protection', 'tech_support', 'streamingTV', 'streaming_movies']]
services = df.melt(
    value_vars=['phone_service', 'multiple_lines', 'online_security', 'online_backup', 
                'device_protection', 'tech_support', 'streamingTV', 'streaming_movies'],
    var_name='service', value_name='usage')
data = services[services['usage'] == 'Yes'].groupby(['service']).size().reset_index(name='count')
fig3 = px.bar(
    data.sort_values(by='count', ascending=False), 
    x='service', y='count',
    title="Количество пользователей по услугам",
    labels={"service": "Услуга", "count": "Количество пользователей"},
    color='count'
)
st.plotly_chart(fig3)

# График 4: Доход по месяцам и годам
revenue = fetch_data_from_view('revenue_by_month_year')
revenue_filtered = revenue[revenue['year'] == year_filter]  # Фильтрация по году
fig4 = px.line(revenue_filtered, x='month', y='total_revenue', color='year',
               title="Доход от услуг по месяцам",
               labels={'month': 'Месяц', 'total_sales': 'Сумма продаж', 'year': 'Год'})
st.plotly_chart(fig4)


# График 5: Распределение оттока['lightblue', 'royalblue', 'lighrcoral']
fig5 = px.histogram(about_churn, x='churn', color='churn', title='Распределение оттока клиентов',
                    labels={'churn': 'Отток'}, template='plotly', width=800, height=600)

st.plotly_chart(fig5)

# График 2: Длительность контракта и отток
fig6 = px.histogram(about_churn, x='tenure', color='churn', barmode='overlay',
                    title='Длительность контракта и отток клиентов',
                    labels={'tenure': 'Длительность контракта (месяцы)', 'churn': 'Отток'},
                    template='plotly', width=800, height=600 )
st.plotly_chart(fig6)

# График 3: Общие траты по оттоку
spending_distribution = fetch_data_from_view('spending_distribution')
spending = spending_distribution.groupby('churn')['total_charges'].sum().reset_index()
# spending = spending.rename(columns={'total_charges': 'total_spent'})

fig7 = px.histogram(    spending_distribution,
    x="total_charges",
    color="churn",
    # marginal="violin", 
    nbins=50,   
    opacity=0.7,      
    histnorm='density', 
    title='Распределение общих трат по оттоку',
    labels={'total_charges': 'Общие траты', 'churn': 'Отток'},
    template='plotly', width=800, height=600)
st.plotly_chart(fig7)


# График 4: Связь между месячными и общими тратами
fig8 = px.scatter(about_churn, x='monthly_charges', y='total_charges', color='churn',
                  title='Месячная и общая плата за услуги (Churn)',
                  labels={'monthly_charges': 'Месячная оплата', 'total_charges': 'Общая плата'},
                  template='plotly', width=800, height=600)
st.plotly_chart(fig8)

# График 5: Отток и поддержка
churn_tech_support = about_churn.groupby(['churn', 'tech_support']).size().reset_index(name='count')
fig9 = px.bar(churn_tech_support, x='churn', y='count', color='tech_support',
              title='Отток клиентов и поддержка',
              labels={'count': 'Количество клиентов', 'churn': 'Отток'}, barmode='group')
st.plotly_chart(fig9)


# График 6: Стриминговые услуги и отток
fig10 = px.scatter(about_churn, x='monthly_charges', y='total_charges', color='streamingTV',
                  title='Месячная и общая плата (Streaming TV)',
                  labels={'monthly_charges': 'Месячная оплата', 'total_charges': 'Общая плата'},
                  template='plotly', width=800, height=600)
st.plotly_chart(fig10)

streamingTV = about_churn.groupby(['churn', 'streamingTV']).size().reset_index(name='count')
fig11 = px.bar(streamingTV, x='churn', y='count', color='streamingTV',
              title='Отток клиентов и Streaming TV',
              labels={'count': 'Количество клиентов', 'churn': 'Отток'}, barmode='group')
st.plotly_chart(fig11)

# График 7: Услуги телефонии и отток
fig12 = px.scatter(about_churn, x='monthly_charges', y='total_charges', color='phone_service',
                  title='Месячная и общая плата (Phone Service)',
                  labels={'monthly_charges': 'Месячная оплата', 'total_charges': 'Общая плата'},
                  template='plotly', width=800, height=600)
st.plotly_chart(fig12)

df_phone_service = about_churn.groupby(['churn', 'phone_service']).size().reset_index(name='count')
fig13 = px.bar(df_phone_service, x='churn', y='count', color='phone_service',
              title='Отток клиентов и Phone Service',
              labels={'count': 'Количество клиентов', 'churn': 'Отток'}, barmode='group')
st.plotly_chart(fig13)

# График 8: Интернет-сервисы и отток
fig14 = px.scatter(about_churn, x='monthly_charges', y='total_charges', color='internet_service',
                   title='Месячная и общая плата (Internet Service)',
                   labels={'monthly_charges': 'Месячная оплата', 'total_charges': 'Общая плата'},
                   template='plotly', width=800, height=600)
st.plotly_chart(fig14)

internet_service = about_churn.groupby(['churn', 'internet_service']).size().reset_index(name='count')
fig15 = px.bar(internet_service, x='churn', y='count', color='internet_service',
               title='Отток клиентов и Internet Service',
               labels={'count': 'Количество клиентов', 'churn': 'Отток'}, barmode='group')
            #    color_discrete_map={'DSL': 'green', 'Fiber optic': 'red', 'No': 'blue'})
st.plotly_chart(fig15)





