CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

CREATE TABLE IF NOT EXISTS bronze.tokopedia_raw (
id SERIAL PRIMARY KEY,
payload JSONB,
observed_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS silver.product_prices (
product_id TEXT,
seller_id TEXT,
price NUMERIC,
observed_at TIMESTAMP,
source_bronze_id INT,
PRIMARY KEY (product_id, seller_id, observed_at)
);

CREATE TABLE IF NOT EXISTS gold.price_momentum (
product_id TEXT,
seller_id TEXT,
current_price NUMERIC,
previous_price NUMERIC,
delta NUMERIC,
observed_at TIMESTAMP,
PRIMARY KEY (product_id, seller_id)
);

CREATE TABLE IF NOT EXISTS gold.price_alerts (
product_id TEXT,
seller_id TEXT,
old_price NUMERIC,
new_price NUMERIC,
drop_pct NUMERIC,
observed_at TIMESTAMP,
PRIMARY KEY (product_id, seller_id)
);
