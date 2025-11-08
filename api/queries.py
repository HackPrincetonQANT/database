# api/queries.py

INSERT_TXN = """
INSERT INTO transactions
(id,user_id,transaction_id,merchant,amount_cents,currency,category,need_or_want,confidence,occurred_at)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

# Note: no LIMIT here; we append it safely in code as a literal integer
GET_FEED_BASE = """
SELECT * FROM transactions
WHERE user_id = %s
ORDER BY occurred_at DESC
"""

UPSERT_REPLY = """
INSERT INTO user_replies (id,transaction_id,user_id,user_label,received_at)
VALUES (%s,%s,%s,%s,%s)
"""

LATEST_REPLY = """
SELECT * FROM user_replies
WHERE transaction_id = %s
ORDER BY received_at DESC, created_at DESC
LIMIT 1
"""

LATEST_PREDICTIONS = """
SELECT * FROM predictions
WHERE user_id = %s
ORDER BY created_at DESC, window_end DESC
"""

# We will compute cutoff_ts in Python and bind it
RECENT_CATEGORY_STATS = """
SELECT
  category,
  COUNT(*) AS txn_count,
  AVG(IFF(need_or_want='want',1,0)) AS want_rate,
  SUM(amount_cents) AS total_cents
FROM transactions
WHERE user_id = %s
  AND occurred_at >= %s
GROUP BY category
ORDER BY total_cents DESC
"""