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
INSERT INTO gold.price_momentum (
    product_id,
    seller_id,
    current_price,
    previous_price,
    delta,
    observed_at
)
SELECT DISTINCT ON (product_id, seller_id)
    product_id,
    seller_id,
    price                                     AS current_price,
    LAG(price) OVER w                         AS previous_price,
    price - LAG(price) OVER w                 AS delta,
    observed_at
FROM silver.product_prices
WINDOW w AS (
    PARTITION BY product_id, seller_id
    ORDER BY observed_at
)
ORDER BY product_id, seller_id, observed_at DESC
ON CONFLICT (product_id, seller_id)
DO UPDATE SET
    previous_price = gold.price_momentum.current_price,
    current_price  = EXCLUDED.current_price,
    delta          = EXCLUDED.current_price - gold.price_momentum.current_price,
    observed_at    = EXCLUDED.observed_at;

""")

conn.commit()
conn.close()
