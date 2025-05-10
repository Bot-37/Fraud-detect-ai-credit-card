import joblib
import pandas as pd
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Logging setup
logger = logging.getLogger("FraudDetection")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/fraud_detector.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
logger.addHandler(file_handler)

class TransactionRequest:
    """Domain object for transaction data."""
    def __init__(self, card_id: str, amount: float, merchant_id: str, timestamp: datetime, 
                 location: Dict[str, Any], device_fingerprint: str, metadata: Dict[str, Any] = {}):
        self.card_id = card_id
        self.amount = amount
        self.merchant_id = merchant_id
        self.timestamp = timestamp
        self.location = location
        self.device_fingerprint = device_fingerprint
        self.metadata = metadata

    def to_feature_dict(self) -> Dict[str, Any]:
        """Converts the transaction request to a feature dictionary for the model."""
        features = {
            'amount': self.amount,
            # Add other features required by the model here
            **{f"V{i}": self.metadata.get(f"V{i}", 0) for i in range(1, 29)}
        }
        return features

class FraudResponse:
    """Domain object for fraud detection response."""
    def __init__(self, transaction_id: str, risk_score: float, is_fraud: bool, reasons: list,
                 model_version: str, timestamp: datetime):
        self.transaction_id = transaction_id
        self.risk_score = risk_score
        self.is_fraud = is_fraud
        self.reasons = reasons
        self.model_version = model_version
        self.timestamp = timestamp

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

    def analyze_transaction(self, transaction: TransactionRequest) -> FraudResponse:
        try:
            # Preprocessing
            features = transaction.to_feature_dict()
            data = pd.DataFrame([features])
            scaled_data = self.scaler.transform(data)

            # Prediction
            probability = self.model.predict_proba(scaled_data)[0][1]
            is_fraud = probability > 0.5
            reasons = ["High risk score"] if is_fraud else []

            return FraudResponse(
                transaction_id=transaction.card_id,
                risk_score=probability,
                is_fraud=is_fraud,
                reasons=reasons,
                model_version="1.0.0",
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logger.error("Error analyzing transaction: %s", traceback.format_exc())
            raise RuntimeError("Failed to analyze transaction.")