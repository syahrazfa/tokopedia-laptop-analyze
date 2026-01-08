# Role: Abnormality Detection Engine
# Function:
# Detects sharp drops and liquidation events.

# Why it exists:
# Arbitrage only exists during panic and mispricing.
# This engine locates market fear.

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
INSERT INTO gold.price_alerts
SELECT
    product_id,
    seller_id,
    previous_price,
    current_price,
    (previous_price - current_price) / previous_price * 100 AS drop_pct,
    observed_at
FROM gold.price_momentum
WHERE previous_price IS NOT NULL
  AND (previous_price - current_price) / previous_price >= 0.10
ON CONFLICT (product_id, seller_id)
DO UPDATE SET
    old_price = EXCLUDED.old_price,
    new_price = EXCLUDED.new_price,
    drop_pct = EXCLUDED.drop_pct,
    observed_at = EXCLUDED.observed_at;
""")

conn.commit()
conn.close()
