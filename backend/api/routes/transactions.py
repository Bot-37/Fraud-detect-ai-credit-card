# app/api/routes/transactions.py

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from app.model.fraud_detector import predict_fraud
from app.utils.logger import logger
from api.routes.auth import get_current_user  # Add this import

router = APIRouter()

@router.post("/predict", dependencies=[Depends(get_current_user)])  # Protect the route
async def predict_transaction(request: Request):
    """
    Accepts a transaction payload and returns fraud prediction.
    """
    try:
        # Step 1: Get JSON data from request
        transaction_data = await request.json()
        logger.info(f"Received transaction data: {transaction_data}")

        # Step 2: Perform prediction
        result = predict_fraud(transaction_data)
        return JSONResponse(content={
            "success": True,
            "prediction": "Fraud" if result["prediction"] == 1 else "Genuine",
            "fraud_probability": result["probability"]
        })

    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(status_code=422, detail=str(ve))

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
