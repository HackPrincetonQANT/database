import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from repo root and from api/ (either will work)
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
load_dotenv(Path(__file__).with_name(".env"))

import snowflake.connector

CFG = dict(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    role=os.getenv("SNOWFLAKE_ROLE"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)

def get_conn():
    return snowflake.connector.connect(**CFG)

def fetch_all(sql: str, params: tuple = ()):
    with get_conn() as conn, conn.cursor(snowflake.connector.DictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()

def execute(sql: str, params: tuple = ()):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        conn.commit()