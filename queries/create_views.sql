-- Анализ клиентской базы 
CREATE OR REPLACE VIEW about_customers AS
select 
    c.customerID,
    c.gender,
    c.senior_citizen,
    c.partner,
    c.dependents,
    f.monthly_charges,
    f.total_charges,
    s.tenure,
    s.device_protection,
    s.online_security,
    s.streamingTV,
    s.internet_service,
    ct.contract,
    EXTRACT(YEAR FROM ct.contract_start_date) AS year,
    SUM(f.monthly_charges) OVER (PARTITION BY c.customerID ORDER BY ct.contract_start_date) AS total_monthly_charges
from customers c
left join financials f on c.customerID = f.customerID
left join services s on c.customerID = s.customerID
left join contracts ct on c.customerID = ct.customerID;


-- Анализ услуг - самые пользуемые услуги по годам
CREATE OR REPLACE VIEW about_services AS
select 
    ct.customerID,
    EXTRACT(YEAR FROM ct.contract_start_date) AS year,
    s.phone_service,
    s.multiple_lines,
    s.internet_service,
    s.online_security,
    s.online_backup,
    s.device_protection,
    s.tech_support,
    s.streamingTV,
    s.streaming_movies
from services s
left join contracts ct  on ct.customerID = s.customerID;

-- Общая сумма дохода от услуг по месяцам и годам
CREATE OR REPLACE VIEW revenue_by_month_year AS
select 
    EXTRACT(YEAR FROM f.last_payment_date) AS year,
    EXTRACT(MONTH FROM f.last_payment_date) AS month,
    SUM(f.monthly_charges) AS total_revenue
from financials f
group by year, month
order by year, month;

--Отчет продаж
CREATE OR REPLACE VIEW sales_report AS
select 
    ct.contract,
    count(distinct c.customerID) as total_customers,
    sum(f.monthly_charges) as total_revenue,
    round(avg(f.monthly_charges), 2) as avg_revenue_per_customer
from contracts ct
left join customers c on ct.customerID = c.customerID
left join financials f on c.customerID = f.customerID
group by ct.contract
order by total_revenue desc;

--Распределение трат по клиентам
CREATE OR REPLACE VIEW spending_distribution AS
select 
    subquery.customerID,
    subquery.monthly_charges,
    subquery.total_charges,
    subquery.churn,
    subquery.year
from (select 
        f.customerID,
        f.monthly_charges,
        f.total_charges,
        f.churn,
        EXTRACT(YEAR FROM ct.contract_start_date) as year
from financials f
left join contracts ct on ct.customerID = f.customerID) as subquery;


--Анализ оттока клиентов
CREATE OR REPLACE VIEW about_churn AS
select
    f.monthly_charges,
    f.total_charges,
    s.internet_service,
    s.phone_service,
    s.streamingTV,
    s.tech_support,
    f.churn,
    s.tenure,
    s.streaming_movies,
    EXTRACT(YEAR FROM ct.contract_start_date) AS year
from financials f
left join services s on f.customerID = s.customerID
left join contracts ct on ct.customerID = f.customerID;

--Создание таблиц вьюшек для странички таблиц
CREATE OR REPLACE VIEW customers2 AS
SELECT * from customers;

CREATE OR REPLACE VIEW services2 AS
SELECT * from services;

CREATE OR REPLACE VIEW contracts2 AS
SELECT * from contracts;

CREATE OR REPLACE VIEW financials2 AS
SELECT * from financials;

CREATE OR REPLACE VIEW payment_methods2 AS
SELECT * from payment_methods;