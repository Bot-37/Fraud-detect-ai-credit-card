# app/api/routes/transactions.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from backend.app.model.fraud_detector import predict_fraud
from backend.app.utils.logger import get_logger
from backend.api.routes.auth import verify_token

router = APIRouter()

# Pydantic model for validating incoming transaction data
class TransactionInput(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount")
    time: str = Field(..., description="Transaction timestamp")
    card_number: str = Field(..., min_length=12, max_length=19)
    merchant_id: str
    card_type: str
    location: str
    user_id: Optional[str] = "anonymous"
    transaction_id: Optional[str] = "txn-0001"

# Pydantic model for response schema (optional)
class PredictionResponse(BaseModel):
    success: bool
    transaction_id: Optional[str]
    prediction: str
    fraud_probability: float
    message: str

@router.post("/predict", response_model=PredictionResponse)
async def predict_transaction(
    transaction: TransactionInput,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Endpoint to predict fraud for a transaction.
    Requires valid authentication token.
    """
    try:
        logger.info(f"User '{current_user['username']}' submitted transaction for prediction: {transaction.dict()}")

        # Call the fraud detection model
        result = predict_fraud(transaction.dict())

        # Validate model output
        if not result or "prediction" not in result or "probability" not in result:
            logger.error("Model returned invalid prediction result")
            raise HTTPException(status_code=400, detail="Invalid model output")

        prediction_label = "Fraud" if result["prediction"] == 1 else "Genuine"

        logger.info(f"Prediction result: {prediction_label} with probability {result['probability']}")

        return {
            "success": True,
            "transaction_id": transaction.transaction_id,
            "prediction": prediction_label,
            "fraud_probability": result["probability"],
            "message": "⚠️ Fraud Detected!" if result["prediction"] == 1 else "✅ Transaction is Safe"
        }

    except HTTPException:
        raise  # Propagate known HTTP exceptions
    except Exception as e:
        logger.error(f"Unexpected error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
