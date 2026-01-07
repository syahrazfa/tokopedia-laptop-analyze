import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

cur.execute("""
INSERT INTO gold.latest_prices
SELECT DISTINCT ON (product_id, seller_id)
    product_id,
    seller_id,
    price,
    observed_at
FROM silver.product_prices
ORDER BY product_id, seller_id, observed_at DESC
ON CONFLICT (product_id, seller_id)
DO UPDATE SET
    latest_price = EXCLUDED.latest_price,
    observed_at = EXCLUDED.observed_at;
""")

conn.commit()
conn.close()
