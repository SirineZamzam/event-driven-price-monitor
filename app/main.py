from fastapi import FastAPI
from app.api import events, decisions, health

app = FastAPI(title="Price Monitor")

app.include_router(events.router, prefix="/events")
app.include_router(decisions.router, prefix="/decisions")
app.include_router(health.router, prefix="/health")