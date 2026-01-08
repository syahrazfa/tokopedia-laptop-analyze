# Role: Capital Activation Layer
# Function:
# Dispatches market signals into execution channels.

# Why it exists:
# Signals without action are worthless.
# This converts intelligence into profit pathways.

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
SELECT product_id, seller_id, old_price, new_price, drop_pct, observed_at
FROM gold.active_price_alerts
""")

alerts = cur.fetchall()

for pid, sid, old, new, drop, ts in alerts:
    msg = f"""
🚨 PRICE DROP ALERT

Product: {pid}
Seller: {sid}
Old: {old}
New: {new}
Drop: {round(drop*100,2)}%
Time: {ts}
"""

    print(msg)

conn.close()
