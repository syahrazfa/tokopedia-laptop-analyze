import requests
import psycopg2

url = "https://www.tokopedia.com/search?st=product&q=laptop"

r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

#CONN PRIVACY
conn = psycopg2.connect(
    dbname="-",
    user="postgres",
    password="-",
    host="localhost",
    port=5432
)

cur = conn.cursor()

cur.execute("""
INSERT INTO bronze.tokopedia_raw (source, raw)
VALUES (%s, %s)
""", ("tokopedia_html_laptop", r.text))

conn.commit()
conn.close()
