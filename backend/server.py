from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.model.fraud_detector import predict_fraud  # Assuming this function handles fraud prediction
from app.utils.logger import get_logger  # Assuming this is for logging
import logging

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logger = get_logger()

# Define the structure of the incoming transaction data
class Transaction(BaseModel):
    amount: float
    time: str
    card_number: str
    merchant_id: str
    card_type: str
    location: str  # Expecting location in the format "latitude, longitude"
    
    # Optional fields (could be added for future extensions)
    user_id: str = None
    transaction_id: str = None

# Route for fraud prediction
@app.post("/predict")
async def predict_transaction(transaction: Transaction):
    """
    Endpoint to predict if a transaction is fraudulent or not.
    Accepts transaction data, including amount, card info, and location.
    """
    try:
        # Log the incoming transaction data (for monitoring purposes)
        logger.info(f"Received transaction data: {transaction.dict()}")

        # Make prediction using the fraud detection model
        prediction_result = predict_fraud(transaction.dict())  # Assuming the function processes the data

        # Check if the prediction result is valid (fraud result should exist)
        if prediction_result:
            fraud_prediction = prediction_result["prediction"]
            fraud_probability = prediction_result["probability"]
        else:
            raise HTTPException(status_code=400, detail="Prediction failed")

        # Log prediction results for monitoring and future improvements
        logger.info(f"Fraud prediction: {fraud_prediction}, Probability: {fraud_probability}")

        # Return the prediction result to the frontend
        return {"prediction": fraud_prediction, "fraud_probability": fraud_probability}

    except Exception as e:
        logger.error(f"Error occurred during fraud prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# For testing if server is working (Health Check)
@app.get("/health")
def read_health():
    return {"status": "OK"}

