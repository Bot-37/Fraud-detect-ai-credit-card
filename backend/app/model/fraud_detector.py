import os
import pickle
import numpy as np
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.logger import get_logger
from app.utils.preprocessing import preprocess_transaction
from app.utils.validator import validate_transaction_input
from app.config import MODEL_PATH
from api.routes.auth import verify_token

# Global model cache to prevent repeated loading
_model = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

def load_model():
    """
    Loads the fraud detection model securely from disk.
    Ensures model is loaded only once.
    """
    global _model
    if _model is None:
        try:
            logger.info("Loading trained fraud detection model...")
            with open(MODEL_PATH, 'rb') as f:
                _model = pickle.load(f)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise RuntimeError("Failed to load fraud detection model.")
    return _model

@router.post("/predict")
async def predict_fraud(transaction_data: dict, token: str = Depends(oauth2_scheme)):
    """
    Predicts whether a transaction is fraudulent.
    """
    # Step 1: Verify Token
    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 2: Validate input
    try:
        validated_input = validate_transaction_input(transaction_data)
    except ValueError as ve:
        logger.warning(f"Invalid input: {ve}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    # Step 3: Preprocess input
    try:
        input_vector = preprocess_transaction(validated_input)
        input_array = np.array([input_vector])  # convert to 2D array
    except Exception as pe:
        logger.error(f"Preprocessing failed: {pe}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Input preprocessing failed")

    # Step 4: Perform prediction
    try:
        model = load_model()
        prediction = model.predict(input_array)[0]
        probability = round(model.predict_proba(input_array)[0][1], 4)  # fraud probability
        logger.info(f"Prediction: {prediction} | Probability: {probability}")
    except Exception as e:
        logger.error(f"Model prediction failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Model prediction error")

    return {
        "prediction": int(prediction),
        "probability": probability
    }
