import os
import pickle
import numpy as np
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from backend.app.utils.logger import get_logger
from backend.app.utils.preprocessing import preprocess_data
from backend.app.utils.validator import validate_dataframe
from backend.app.config import Config
from backend.app.utils.security import verify_token


# --- Constants & Globals ---
_model = None
MODEL_PATH = Config.MODEL_PATH
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()
logger = get_logger("fraud_detector")  # ✅ Only initialized once

# --- Load Model ---
def load_model():
    """
    Load the trained model from disk once and reuse from memory.
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

# --- Prediction Endpoint ---
@router.post("/predict")
async def predict_fraud(transaction_data: dict, token: str = Depends(oauth2_scheme)):
    """
    Predict whether a transaction is fraudulent.
    """
    # Step 1: Verify Token
    try:
        user = verify_token(token)  # ⚠️ Undefined: should be imported
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 2: Validate Input
    try:
        validated_input = validate_dataframe(transaction_data)
        logger.info(f"Validated input data: {validated_input}")
    except ValueError as ve:
        logger.warning(f"Invalid input data: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(ve)}"
        )

    # Step 3: Preprocess Input
    try:
        input_vector = preprocess_data(validated_input)
        input_array = np.array([input_vector])
        logger.info(f"Preprocessed input vector: {input_vector}")
    except Exception as pe:
        logger.error(f"Preprocessing failed: {pe}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Input preprocessing failed"
        )

    # Step 4: Predict
    try:
        model = load_model()
        prediction = model.predict(input_array)[0]
        probability = round(model.predict_proba(input_array)[0][1], 4)
        logger.info(f"Prediction: {prediction} | Probability: {probability}")
    except Exception as e:
        logger.error(f"Model prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model prediction error"
        )

    # Step 5: Validate Prediction
    if prediction not in [0, 1]:
        logger.error(f"Invalid prediction value: {prediction}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid prediction value returned by model"
        )

    return {
        "prediction": int(prediction),
        "probability": probability
    }
