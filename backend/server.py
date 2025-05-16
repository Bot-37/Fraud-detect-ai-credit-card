import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.model.fraud_detector import predict_fraud
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  
from backend.app.utils.logger import get_logger

# === Initialize FastAPI ===
app = FastAPI(title="Credit Card Fraud Detection API", version="1.0.0")

# === Enable CORS for React Frontend ===
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Logger ===
logger = get_logger(__name__)

# === Pydantic Schema for Transaction Input ===
class Transaction(BaseModel):
    amount: float
    time: str
    card_number: str
    merchant_id: str
    card_type: str
    location: str
    user_id: str = None
    transaction_id: str = None

# === API Router with prefix /api ===
api_router = APIRouter(prefix="/api")

@api_router.post("/predict")
async def predict_transaction(transaction: Transaction):
    try:
        logger.info(f"[INPUT] Transaction received: {transaction.dict()}")

        model_input = {
            "amount": transaction.amount,
            "time": transaction.time,
            "card_number": transaction.card_number,
            "merchant_id": transaction.merchant_id,
            "card_type": transaction.card_type,
            "location": transaction.location,
            "user_id": transaction.user_id or "anonymous",
            "transaction_id": transaction.transaction_id or "txn-0001"
        }

        prediction_result = predict_fraud(model_input)

        if not prediction_result or "prediction" not in prediction_result or "probability" not in prediction_result:
            raise HTTPException(status_code=400, detail="Invalid model output")

        fraud_prediction = prediction_result["prediction"]
        fraud_probability = prediction_result["probability"]

        logger.info(f"[OUTPUT] Prediction: {fraud_prediction}, Probability: {fraud_probability}")

        if fraud_prediction == 1:
            logger.warning(f"Transaction {model_input['transaction_id']} blocked: Fraud detected")
            raise HTTPException(
                status_code=403,
                detail=f"Transaction blocked: Fraudulent transaction detected with probability {fraud_probability}"
            )

        return {
            "status": "approved",
            "data": {
                "transaction_id": model_input["transaction_id"],
                "fraud_prediction": fraud_prediction,
                "fraud_probability": fraud_probability,
                "message": "✅ Transaction is Safe"
            }
        }

    except HTTPException as http_err:
        logger.warning(f"[WARNING] HTTP Error: {str(http_err)}")
        raise http_err
    except Exception as err:
        logger.error(f"[ERROR] Unexpected Exception: {str(err)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@api_router.get("/health")
def health_check():
    return {"status": "OK", "message": "Fraud Detection API is Live"}

# === Include the router in the app ===
app.include_router(api_router)
