from pydantic import BaseModel
from typing import Optional

# Define the structure of the transaction data
class Transaction(BaseModel):
    amount: float
    time: str
    card_number: str
    merchant_id: str
    card_type: str
    location: Optional[str] = None  # optional field, you can modify this based on the data you're receiving

# This schema can be used for validating incoming transaction data in the `/predict` endpoint
