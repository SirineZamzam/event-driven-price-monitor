from app.db.connection import get_conn
from app.ai.summarize import summarize_price_change

def get_unprocessed_event(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, source, item, old_price, new_price, currency
        FROM events
        WHERE processed = false
        ORDER BY observed_at
        LIMIT 1
    """)
    row = cur.fetchone()
    cur.close()
    return row

def mark_event_processed(conn, event_id):
    cur = conn.cursor()
    cur.execute("""
        UPDATE events
        SET processed = true
        WHERE id = %s
    """, (event_id,))
    conn.commit()
    cur.close()

def insert_decision(conn, event_id, summary, model, prompt):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO decisions (event_id, summary, model, prompt)
        VALUES (%s, %s, %s, %s)
    """, (event_id, summary, model, prompt))
    conn.commit()
    cur.close()

def main():
    conn = get_conn()
    event = get_unprocessed_event(conn)

    if not event:
        print("No events to process")
        conn.close()
        return

    event_id, source, item, old_price, new_price, currency = event
    print("Processing event:", event)

    # AI summary
    summary, prompt, model = summarize_price_change(
        source, item, old_price, new_price, currency
    )

    recommendation = None

    if old_price is not None:
        if new_price < old_price:
            recommendation = "Consider buying."
        elif new_price > old_price:
            recommendation = "Consider waiting."
        else:
            recommendation = "No action needed."

    # Combine summary + recommendation
    if recommendation:
        summary = f"{summary} Recommendation: {recommendation}"

    # Save decision
    insert_decision(conn, event_id, summary, model, prompt)
    mark_event_processed(conn, event_id)

    print("AI Summary:", summary)
    print("Decision saved")

    conn.close()

if __name__ == "__main__":
    main()