# api/main.py
from fastapi import FastAPI, HTTPException
from .models import TransactionInsert, UserReply
from .db import execute, fetch_all
from . import queries as Q
from datetime import datetime, timedelta, timezone

app = FastAPI(title="BalanceIQ Snowflake API")

@app.get("/health")
def health():
    try:
        rows = fetch_all(
            "SELECT CURRENT_USER() AS U, CURRENT_ROLE() AS R, CURRENT_WAREHOUSE() AS W, "
            "CURRENT_DATABASE() AS D, CURRENT_SCHEMA() AS S"
        )
        return rows[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transactions/insert")
def insert_transaction(txn: TransactionInsert):
    try:
        execute(Q.INSERT_TXN, (
            txn.id, txn.user_id, txn.transaction_id, txn.merchant,
            txn.amount_cents, txn.currency, txn.category, txn.need_or_want,
            txn.confidence, txn.occurred_at
        ))
        return {"ok": True, "id": txn.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feed")
def get_feed(user_id: str, limit: int = 20):
    try:
        # clamp limit and append as literal (Snowflake disallows bind in LIMIT)
        n = max(1, min(limit, 200))
        sql = Q.GET_FEED_BASE + f"\nLIMIT {n}"
        return fetch_all(sql, (user_id,))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/replies/upsert")
def upsert_reply(payload: UserReply):
    try:
        execute(Q.UPSERT_REPLY, (
            payload.id, payload.transaction_id, payload.user_id,
            payload.user_label, payload.received_at
        ))
        return {"ok": True, "id": payload.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/replies/latest")
def latest_reply(transaction_id: str):
    try:
        rows = fetch_all(Q.LATEST_REPLY, (transaction_id,))
        return rows[0] if rows else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predictions")
def latest_predictions(user_id: str):
    try:
        return fetch_all(Q.LATEST_PREDICTIONS, (user_id,))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/category")
def recent_category_stats(user_id: str, days: int = 30):
    try:
        # compute cutoff_ts (UTC) and bind as timestamp
        d = max(1, min(days, 365))
        cutoff_ts = datetime.now(timezone.utc) - timedelta(days=d)
        return fetch_all(Q.RECENT_CATEGORY_STATS, (user_id, cutoff_ts))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))