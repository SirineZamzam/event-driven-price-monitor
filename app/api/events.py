from fastapi import APIRouter
from app.db.connection import get_conn

router = APIRouter()

@router.get("/")
def list_events():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, source, item, old_price, new_price, currency, observed_at, processed
        FROM events
        ORDER BY observed_at DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "source": r[1],
            "item": r[2],
            "old_price": float(r[3]) if r[3] else None,
            "new_price": float(r[4]),
            "currency": r[5],
            "observed_at": r[6],
            "processed": r[7]
        }
        for r in rows
    ]