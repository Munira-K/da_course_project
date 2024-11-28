-- Создание таблицы customers
CREATE TABLE customers (
    customerID STRING PRIMARY KEY,
    gender STRING,
    senior_citizen INTEGER,
    partner STRING,
    dependents STRING
);

-- Создание таблицы services
CREATE TABLE services (
    customerID STRING,
    tenure INTEGER,
    phone_service STRING,
    multiple_lines STRING,
    internet_service STRING,
    online_security STRING,
    online_backup STRING,
    device_protection STRING,
    tech_support STRING,
    streamingTV STRING,
    streaming_movies STRING,
    FOREIGN KEY (customerID) REFERENCES customers(customerID) 
);

-- Создание таблицы contracts
CREATE TABLE contracts (
    customerID STRING,
    contract STRING,
    paperless_billing STRING,
    payment_method_id INTEGER,
    contract_start_date DATE,
    contract_end_date DATE,
    FOREIGN KEY (customerID) REFERENCES customers(customerID) 
);

-- Создание таблицы financials
CREATE TABLE financials (
    customerID STRING,
    monthly_charges FLOAT,
    total_charges FLOAT,
    churn STRING,
    last_payment_date DATE,
    FOREIGN KEY (customerID) REFERENCES customers(customerID)
);

-- Создание таблицы payment_methods
CREATE TABLE payment_methods (
    payment_method_id INTEGER PRIMARY KEY,
    payment_method STRING
);
