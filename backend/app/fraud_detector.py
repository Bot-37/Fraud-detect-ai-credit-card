import joblib
import pandas as pd
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Logging setup
logger = logging.getLogger("FraudDetection")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/fraud_detector.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
logger.addHandler(file_handler)

class FraudDetectionSystem:
    def __init__(self, model_path: str, scaler_path: str):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self._initialize_system()

    def _initialize_system(self):
        try:
            logger.info("Initializing Fraud Detection System...")
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            logger.info("Model and scaler loaded successfully.")
        except Exception as e:
            logger.error("Error initializing system: %s", traceback.format_exc())
            raise RuntimeError("Failed to initialize Fraud Detection System.")

    def analyze_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Validation
            required_features = ['amount'] + [f"V{i}" for i in range(1, 29)]
            missing_features = [f for f in required_features if f not in transaction]
            if missing_features:
                raise ValueError(f"Missing required features: {missing_features}")

            # Preprocessing
            data = pd.DataFrame([transaction])
            scaled_data = self.scaler.transform(data)

            # Prediction
            probability = self.model.predict_proba(scaled_data)[0][1]
            is_fraud = probability > 0.5

            return {
                "probability": probability,
                "is_fraud": is_fraud,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error("Error analyzing transaction: %s", traceback.format_exc())
            raise RuntimeError("Failed to analyze transaction.")