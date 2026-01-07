import requests
import psycopg2
import json
import time
import os
from dotenv import load_dotenv

URL = "https://gql.tokopedia.com/graphql"

KEYWORDS = [
    "laptop",
    "gaming laptop",
    "macbook",
    "ultrabook",
    "laptop i5",
    "laptop ryzen"
]

CITIES = [176, 178, 181]   # Jakarta Barat, Jakarta Selatan, Jakarta Timur
PAGES = [1, 2, 3, 4, 5]

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

for city in CITIES:
    for keyword in KEYWORDS:
        for page in PAGES:

            params = (
                f"device=desktop&enter_method=normal_search&ob=23"
                f"&page={page}&q={keyword}"
                f"&rows=60&safe_search=false&source=search&st=product"
                f"&user_cityId={city}"
            )

            payload = [{
                "operationName": "SearchProductV5Query",
                "variables": {"params": params},
                "query": """query SearchProductV5Query($params: String!) {
                  searchProductV5(params: $params) {
                    data {
                      products {
                        id
                        name
                        shop { id name city }
                        price { number }
                        stock { ttsSKUID }
                      }
                    }
                  }
                }"""
            }]

            r = requests.post(URL, json=payload, headers=headers, timeout=30)
            r.raise_for_status()

            cur.execute("""
            INSERT INTO bronze.tokopedia_raw (source, raw)
            VALUES (%s, %s)
            """, ("tokopedia_search_json", json.dumps(r.json())))

            conn.commit()
            time.sleep(1)

conn.close()
