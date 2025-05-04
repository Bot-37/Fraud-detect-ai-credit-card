# app/detector.py
import pandas as pd
import joblib
import logging
import os
import traceback
import numpy as np
from datetime import datetime
from sklearn.base import BaseEstimator
from typing import Dict, Union, List, Any, Optional, Tuple

class AdvancedFraudDetector:
    """
    Industrial-Standard Fraud Detection System with Enhanced Features
    """
    
    def __init__(self, model_path: str, scaler_path: str):
        # Initialize logging system
        self.logger = logging.getLogger("AdvancedFraudDetector")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
            
            # File handler
            file_handler = logging.FileHandler('logs/advanced_fraud.log')
            file_handler.setFormatter(formatter)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

        # Load ML artifacts
        self.model, self.scaler = self._load_artifacts(model_path, scaler_path)
        self.expected_features = list(self.scaler.feature_names_in_)
        self.known_fraudulent_cards = set()
        
        # Initialize business rules
        self.fraud_threshold = 0.85
        self.geo_threshold_km = 500  # For production, use geopy instead
        self.card_age_threshold = 90  # Days until expiration

    def _load_artifacts(self, model_path: str, scaler_path: str):
        """Load ML artifacts with error handling"""
        try:
            self.logger.info("🔧 Loading ML artifacts...")
            return joblib.load(model_path), joblib.load(scaler_path)
        except Exception as e:
            self.logger.error("❌ Failed to load artifacts")
            self.logger.error(traceback.format_exc())
            raise RuntimeError("Critical initialization error")

    def process_transaction(self, card_data: Dict, transaction_data: Dict) -> Dict:
        """End-to-end transaction processing"""
        try:
            # Immediate block for known fraud cards
            if str(card_data.get('id')) in self.known_fraudulent_cards:
                return self._fraud_response("Pre-registered fraudulent card")
            
            # Feature engineering
            features = self._create_features(card_data, transaction_data)
            scaled_features = self._scale_features(features)
            
            # Model prediction
            prediction = self.model.predict_proba(scaled_features)[0][1]
            
            # Apply business rules
            return self._apply_rules(prediction, card_data, transaction_data)
            
        except Exception as e:
            self.logger.error(f"Transaction processing failed: {str(e)}")
            return self._error_response()

    def _create_features(self, card_data: Dict, tx_data: Dict) -> pd.DataFrame:
        """Create engineered features"""
        return pd.DataFrame([{
            'card_age': self._calculate_card_age(card_data['expiry_date']),
            'amount_ratio': tx_data['amount'] / 100000,
            'cvv_mismatch': int(tx_data.get('cvv', '') != card_data['cvv']),
            'geo_risk': self._calculate_geo_risk(card_data, tx_data),
            'tx_frequency': tx_data.get('hourly_count', 0),
            'Amount': tx_data['amount']
        }])

    def _calculate_card_age(self, expiry: str) -> float:
        """Calculate days until card expiration"""
        expiry_date = datetime.strptime(expiry, "%m/%y")
        return (expiry_date - datetime.now()).days

    def _calculate_geo_risk(self, card_data: Dict, tx_data: Dict) -> float:
        """Simplified geographic risk calculation"""
        # For production: Implement proper geocoding
        return np.random.uniform(0, 1)  # Placeholder

    def _scale_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Apply feature scaling"""
        return pd.DataFrame(
            self.scaler.transform(features[self.expected_features]),
            columns=self.expected_features
        )

    def _apply_rules(self, probability: float, card_data: Dict, tx_data: Dict) -> Dict:
        """Apply business rules to prediction"""
        final_verdict = probability >= self.fraud_threshold
        reason = "High probability" if final_verdict else "Within normal parameters"
        
        return {
            'fraud_probability': probability,
            'final_verdict': final_verdict,
            'reason': reason,
            'threshold': self.fraud_threshold,
            'card_id': card_data.get('id'),
            'timestamp': datetime.now().isoformat()
        }

    def update_fraud_list(self, card_ids: List[str]):
        """Update known fraudulent cards list"""
        self.known_fraudulent_cards.update(map(str, card_ids))
        self.logger.info(f"Updated fraud list with {len(card_ids)} new entries")

    def _fraud_response(self, reason: str) -> Dict:
        """Standard fraud response template"""
        return {
            'fraud_probability': 1.0,
            'final_verdict': True,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }

    def _error_response(self) -> Dict:
        """Error response template"""
        return {
            'fraud_probability': 0.0,
            'final_verdict': False,
            'reason': 'System error',
            'timestamp': datetime.now().isoformat()
        }