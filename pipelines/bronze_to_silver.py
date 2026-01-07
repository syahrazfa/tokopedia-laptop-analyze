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
SELECT id, raw, extracted_at
FROM bronze.tokopedia_raw
WHERE source = 'tokopedia_search_json'
AND id NOT IN (
    SELECT DISTINCT source_bronze_id
    FROM silver.product_prices
    WHERE source_bronze_id IS NOT NULL
)
ORDER BY id;

""")

bronze_rows = cur.fetchall()

for bronze_id, raw_json_text, extracted_at in bronze_rows:

    world = json.loads(raw_json_text)
    products = world[0]["data"]["searchProductV5"]["data"]["products"]

    if not products:
        continue

    for product in products:
        product_id = product["id"]
        seller_id = product["shop"]["id"]
        price = product["price"]["number"]

        observed_at = extracted_at
        source_bronze_id = bronze_id

        cur.execute("""
        INSERT INTO silver.product_prices (
            product_id,
            seller_id,
            price,
            observed_at,
            source_bronze_id
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
        """, (
            product_id,
            seller_id,
            price,
            observed_at,
            source_bronze_id
        ))

conn.commit()
conn.close()


