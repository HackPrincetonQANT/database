from pydantic import BaseModel, Field

class TransactionInsert(BaseModel):
    id: str
    user_id: str
    transaction_id: str
    merchant: str
    amount_cents: int
    currency: str = "USD"
    category: str
    need_or_want: str = Field(pattern="^(need|want|unknown)$")
    confidence: float = 1.0
    occurred_at: str  # ISO datetime

class UserReply(BaseModel):
    id: str
    transaction_id: str
    user_id: str
    user_label: str = Field(pattern="^(need|want|unknown)$")
    received_at: str  # ISO datetime