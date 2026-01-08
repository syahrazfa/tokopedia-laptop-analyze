# Role: Fallback Intelligence Sensor
# Function:
# Secondary extraction path for pages not available via GraphQL.

# Why it exists:
# Markets mutate. APIs die. HTML never disappears.
# This is your anti-fragility sensor.

import requests
import psycopg2
import os
from dotenv import load_dotenv

url = "https://www.tokopedia.com/search?st=product&q=laptop"

r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

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
INSERT INTO bronze.tokopedia_raw (source, raw)
VALUES (%s, %s)
""", ("tokopedia_html_laptop", r.text))

conn.commit()
conn.close()
