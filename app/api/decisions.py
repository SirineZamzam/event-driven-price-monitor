from fastapi import APIRouter
from app.db.connection import get_conn

router = APIRouter()

@router.get("/")
def list_decisions():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, event_id, summary, model, prompt, created_at
        FROM decisions
        ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "event_id": r[1],
            "summary": r[2],
            "model": r[3],
            "prompt": r[4],
            "created_at": r[5]
        }
        for r in rows
    ]