import os
import sys
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from backend.app.model.fraud_detector import predict_fraud, load_model
from backend.app.utils.logger import get_logger

# === Setup System Path for Imports ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# === Initialize FastAPI App ===
app = FastAPI(
    title="Credit Card Fraud Detection API",
    version="1.0.0",
    description="Predicts if a credit card transaction is fraudulent."
)

# === CORS Configuration ===    
FRONTEND_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# === Logger ===
logger = get_logger(__name__)

# === Pydantic Schema ===
class Transaction(BaseModel):
    amount: float
    time: str
    card_number: str
    merchant_id: str
    card_type: str
    location: str
    user_id: Optional[str] = "anonymous"
    transaction_id: Optional[str] = "txn-0001"
    card_holder_name: Optional[str] = None
    merchant_name: Optional[str] = None
    merchant_category: Optional[str] = None

# === API Router ===
api_router = APIRouter(prefix="/api")

@api_router.post("/predict")
async def predict_transaction(transaction: Transaction):
    try:
        logger.info(f"[INPUT] Transaction received: {transaction.dict()}")

        # ✅ Await the coroutine
        prediction_result = await predict_fraud(transaction.dict())

        if not prediction_result or "prediction" not in prediction_result or "probability" not in prediction_result:
            logger.error(f"[ERROR] Invalid model output: {prediction_result}")
            raise HTTPException(status_code=400, detail="Invalid model output")

        prediction = prediction_result["prediction"]
        probability = prediction_result["probability"]
        logger.info(f"[OUTPUT] Prediction: {prediction}, Probability: {probability}")

        if prediction == 1:
            logger.warning(f"[FRAUD] Transaction {transaction.transaction_id} BLOCKED (Probability: {probability})")
            return JSONResponse(
                status_code=403,
                content={
                    "status": "blocked",
                    "data": {
                        "transaction_id": transaction.transaction_id,
                        "fraud_prediction": prediction,
                        "fraud_probability": probability,
                        "message": f"❌ Transaction blocked: Fraudulent with probability {probability}"
                    }
                }
            )

        return {
            "status": "approved",
            "data": {
                "transaction_id": transaction.transaction_id,
                "fraud_prediction": prediction,
                "fraud_probability": probability,
                "message": "✅ Transaction is Safe"
            }
        }

    except HTTPException as http_err:
        logger.warning(f"[HTTP ERROR] {str(http_err)}")
        raise http_err
    except Exception as err:
        logger.error(f"[UNEXPECTED ERROR] {str(err)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Internal Server Error",
                "detail": str(err)
            }
        )

@api_router.get("/health")
def health_check():
    """
    Checks whether the ML model loads correctly.
    """
    try:
        load_model()
        return {"status": "OK", "message": "Fraud Detection API is Live"}
    except Exception as e:
        logger.error(f"[HEALTH CHECK ERROR] {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "ERROR",
                "message": f"Model load failed: {str(e)}"
            }
        )

@api_router.get("/status")
def model_status():
    """
    Extra endpoint to verify model integrity and metadata (if supported).
    """
    try:
        model = load_model()
        return {"status": "OK", "message": "Model Loaded", "model": str(model)}
    except Exception as e:
        logger.error(f"[STATUS ERROR] {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "ERROR",
                "message": f"Could not load model: {str(e)}"
            }
        )

# === Register Routes ===
app.include_router(api_router)
