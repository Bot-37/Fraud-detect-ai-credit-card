import os
import pickle
import numpy as np
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.utils.logger import get_logger
from app.utils.preprocessing import preprocess_data
from app.utils.validator import validate_dataframe
from app.config import Config

# Global model cache to prevent repeated loading
_model = None
MODEL_PATH = Config.MODEL_PATH  # ✅ Correctly set model path from Config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

def load_model():
    """
    Loads the fraud detection model securely from disk.
    Ensures model is loaded only once.
    """
    global _model
    if _model is None:
        logger = get_logger()
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
    logger = get_logger()

    # Step 1: Verify Token (using the function from auth.py)
    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 2: Validate input (using validate_dataframe from utils)
    try:
        validated_input = validate_dataframe(transaction_data)
    except ValueError as ve:
        logger.warning(f"Invalid input: {ve}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    # Step 3: Preprocess input data (using preprocess_data from utils)
    try:
        input_vector = preprocess_data(validated_input)
        input_array = np.array([input_vector])  # Convert to 2D array for prediction
    except Exception as pe:
        logger.error(f"Preprocessing failed: {pe}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Input preprocessing failed")

    # Step 4: Perform prediction
    try:
        model = load_model()  # Load the model if not already loaded
        prediction = model.predict(input_array)[0]
        probability = round(model.predict_proba(input_array)[0][1], 4)  # Fraud probability
        logger.info(f"Prediction: {prediction} | Probability: {probability}")
    except Exception as e:
        logger.error(f"Model prediction failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Model prediction error")

    # Return prediction result
    return {
        "prediction": int(prediction),  # Fraud = 1, Genuine = 0
        "probability": probability
    }
