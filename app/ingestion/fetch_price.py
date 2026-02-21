import requests
from app.db.connection import get_conn

# Multiple real products from FakeStore API
PRODUCTS = [
    {
        "source": "fakestoreapi",
        "item": "product_1",
        "currency": "USD",
        "url": "https://fakestoreapi.com/products/1"
    },
    {
        "source": "fakestoreapi",
        "item": "product_2",
        "currency": "USD",
        "url": "https://fakestoreapi.com/products/2"
    },
    {
        "source": "fakestoreapi",
        "item": "product_3",
        "currency": "USD",
        "url": "https://fakestoreapi.com/products/3"
    },
    {
        "source": "fakestoreapi",
        "item": "product_4",
        "currency": "USD",
        "url": "https://fakestoreapi.com/products/4"
    }
]

def fetch_current_price(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return float(data["price"])

def get_last_price(conn, source, item):
    cur = conn.cursor()
    cur.execute("""
        SELECT new_price
        FROM events
        WHERE source = %s AND item = %s
        ORDER BY observed_at DESC
        LIMIT 1
    """, (source, item))
    row = cur.fetchone()
    cur.close()
    return row[0] if row else None

def insert_event(conn, source, item, old_price, new_price, currency):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO events (source, item, old_price, new_price, currency)
        VALUES (%s, %s, %s, %s, %s)
    """, (source, item, old_price, new_price, currency))
    conn.commit()
    cur.close()

def main():
    conn = get_conn()

    THRESHOLD = 0.05  # 5% minimum change required

    for product in PRODUCTS:
        source = product["source"]
        item = product["item"]
        currency = product["currency"]
        url = product["url"]

        try:
            current_price = fetch_current_price(url)
            last_price = get_last_price(conn, source, item)

            if current_price is None:
                print(f"[{item}] Failed to fetch price")
                continue

            if last_price is None:
                print(f"[{item}] First price: {current_price}")
                insert_event(conn, source, item, None, current_price, currency)

            else:
                percent_change = abs((current_price - last_price) / last_price)

                if percent_change < THRESHOLD:
                    print(f"[{item}] Change below threshold ({percent_change:.2%}) — Ignored")
                else:
                    print(
                        f"[{item}] Significant change ({percent_change:.2%}): "
                        f"{last_price} -> {current_price}"
                    )
                    insert_event(conn, source, item, last_price, current_price, currency)

        except Exception as e:
            print(f"[{item}] Error fetching price: {e}")

    conn.close()

if __name__ == "__main__":
    main()