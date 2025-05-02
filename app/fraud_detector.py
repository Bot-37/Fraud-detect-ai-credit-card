# app/detector.py
import pandas as pd
import joblib
import logging
import os
import traceback
from datetime import datetime
from sklearn.base import BaseEstimator
from typing import Dict, Union, List, Any, Optional, Tuple
import numpy as np

# === Setup Logging ===
# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

logger = logging.getLogger("FraudDetector")
logger.setLevel(logging.INFO)

# File handler for persistent logs
file_handler = logging.FileHandler(os.path.join('logs', 'fraud_detector.log'))
file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
logger.addHandler(file_handler)

# Console handler for immediate feedback
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
logger.addHandler(console_handler)

class FraudDetector:
    """
    Industrial-standard Credit Card Fraud Detection System
    
    This class handles the detection of fraudulent credit card transactions
    using a pre-trained machine learning model.
    """
    
    def __init__(self, model_path: str = "model/fraud_model.pkl", scaler_path: str = "model/scaler.pkl"):
        """
        Initialize the fraud detector with model and scaler.
        
        Args:
            model_path: Path to the trained model file
            scaler_path: Path to the fitted scaler file
        """
        try:
            logger.info("🚀 Initializing Fraud Detection System...")
            self.model: BaseEstimator = joblib.load(model_path)
            logger.info("✅ Model loaded successfully")
        except Exception as e:
            logger.error("❌ Failed to load model")
            logger.error(traceback.format_exc())
            raise e
            
        try:
            self.scaler = joblib.load(scaler_path)
            logger.info("✅ Scaler loaded successfully")
            
            # Store feature names from scaler for validation
            self.expected_features = list(self.scaler.feature_names_in_)
            logger.info(f"✅ Loaded {len(self.expected_features)} expected features")
        except Exception as e:
            logger.error("❌ Failed to load scaler")
            logger.error(traceback.format_exc())
            raise e
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess transaction data for prediction.
        
        Args:
            df: DataFrame containing transaction data
            
        Returns:
            Preprocessed DataFrame ready for model prediction
        """
        try:
            logger.info("🔄 Preprocessing transaction data...")
            df_copy = df.copy()
            
            # Check for Time column and remove if present (as in training)
            if 'Time' in df_copy.columns:
                df_copy = df_copy.drop('Time', axis=1)
                logger.info("ℹ️ 'Time' column removed as per training procedure")
            
            # Check for Class column and remove if present
            if 'Class' in df_copy.columns:
                df_copy = df_copy.drop('Class', axis=1)
                logger.info("ℹ️ 'Class' column removed as it's the target variable")
            
            # Validate that all expected features are present
            missing = set(self.expected_features) - set(df_copy.columns)
            if missing:
                raise ValueError(f"❌ Missing expected features: {missing}")
            
            # Remove any extra columns that weren't in training
            extra = set(df_copy.columns) - set(self.expected_features)
            if extra:
                logger.warning(f"⚠️ Removing extra columns not used in training: {extra}")
                df_copy = df_copy.drop(extra, axis=1)
            
            # Reorder columns to match training set order
            df_copy = df_copy[self.expected_features]
            
            # Apply scaler to the feature set
            scaled_array = self.scaler.transform(df_copy)
            scaled_df = pd.DataFrame(scaled_array, columns=self.expected_features)
            
            logger.info("✅ Preprocessing completed successfully")
            return scaled_df
            
        except Exception as e:
            logger.error("❌ Error during preprocessing")
            logger.error(traceback.format_exc())
            raise e
    
    def detect_fraud(self, transaction: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Detect fraudulent transactions.
        
        Args:
            transaction: DataFrame or dictionary containing transaction data
            
        Returns:
            Dictionary with prediction results including fraud status, probability, and metadata
        """
        try:
            # Convert input to DataFrame if it's a dictionary
            transaction_df = transaction
            transaction_id = None
            
            if isinstance(transaction, dict):
                transaction_id = transaction.get('transaction_id', 'unknown')
                transaction_df = pd.DataFrame([transaction])
                logger.info(f"🔄 Processing single transaction: {transaction_id}")
            elif isinstance(transaction, list):
                transaction_df = pd.DataFrame(transaction)
                logger.info(f"🔄 Processing batch of {len(transaction)} transactions")
            
            # Extract transaction_id if present in DataFrame
            if isinstance(transaction_df, pd.DataFrame) and 'transaction_id' in transaction_df.columns:
                transaction_id = transaction_df['transaction_id'].iloc[0]
                transaction_df = transaction_df.drop('transaction_id', axis=1)
            
            # Preprocess the data
            preprocessed_df = self.preprocess_data(transaction_df)
            
            # Get prediction and probability
            prediction = self.model.predict(preprocessed_df)
            fraud_probability = self.model.predict_proba(preprocessed_df)[:, 1]
            
            # Format results
            result = {
                'is_fraud': bool(prediction[0] == 1),
                'fraud_probability': float(fraud_probability[0]),
                'transaction_id': transaction_id,
                'verdict': "Fraudulent" if prediction[0] == 1 else "Legitimate",
                'timestamp': datetime.now().isoformat()
            }
            
            # Log the result
            verdict_emoji = "🚨" if result['is_fraud'] else "✅"
            logger.info(f"{verdict_emoji} Prediction: {result['verdict']} (probability: {result['fraud_probability']:.4f}) for transaction: {transaction_id}")
            
            return result
            
        except Exception as e:
            logger.error("❌ Error during fraud detection")
            logger.error(traceback.format_exc())
            raise e
    
    def detect_fraud_batch(self, transactions: Union[pd.DataFrame, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Process a batch of transactions.
        
        Args:
            transactions: DataFrame or list of dictionaries containing transaction data
            
        Returns:
            List of prediction results for each transaction
        """
        try:
            logger.info(f"🔄 Processing batch of transactions")
            
            if isinstance(transactions, list):
                transactions_df = pd.DataFrame(transactions)
            else:
                transactions_df = transactions.copy()
            
            # Keep track of transaction IDs if present
            transaction_ids = None
            if 'transaction_id' in transactions_df.columns:
                transaction_ids = transactions_df['transaction_id'].tolist()
                transactions_df = transactions_df.drop('transaction_id', axis=1)
            
            # Preprocess all data at once
            preprocessed_df = self.preprocess_data(transactions_df)
            
            # Get predictions and probabilities
            predictions = self.model.predict(preprocessed_df)
            fraud_probabilities = self.model.predict_proba(preprocessed_df)[:, 1]
            
            # Format results
            results = []
            for i in range(len(predictions)):
                transaction_id = transaction_ids[i] if transaction_ids else f"tx_{i}"
                result = {
                    'is_fraud': bool(predictions[i] == 1),
                    'fraud_probability': float(fraud_probabilities[i]),
                    'transaction_id': transaction_id,
                    'verdict': "Fraudulent" if predictions[i] == 1 else "Legitimate",
                    'timestamp': datetime.now().isoformat()
                }
                results.append(result)
            
            # Log summary
            fraud_count = sum(1 for r in results if r['is_fraud'])
            logger.info(f"✅ Batch processing complete: {fraud_count} fraudulent out of {len(results)} transactions")
            
            return results
            
        except Exception as e:
            logger.error("❌ Error during batch fraud detection")
            logger.error(traceback.format_exc())
            raise e
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from the model if available.
        
        Returns:
            Dictionary mapping feature names to importance scores
        """
        try:
            if hasattr(self.model, 'feature_importances_'):
                importance = self.model.feature_importances_
                importance_dict = dict(zip(self.expected_features, importance))
                return importance_dict
            else:
                logger.warning("⚠️ Feature importance not available for this model type")
                return {}
        except Exception as e:
            logger.error("❌ Error retrieving feature importance")
            logger.error(traceback.format_exc())
            return {}
    
    def evaluate_transaction(self, transaction: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Evaluate a transaction with detailed reasoning.
        
        Args:
            transaction: Dictionary containing transaction data
            
        Returns:
            Tuple of decision and explanation dictionary
        """
        try:
            # Get the basic fraud detection result
            result = self.detect_fraud(transaction)
            
            # For models that support feature importance per prediction (like TreeExplainer)
            explanation = {
                'top_factors': self._get_top_contributing_factors(transaction),
                'threshold': 0.5,  # Default threshold, could be configurable
                'model_confidence': "High" if abs(result['fraud_probability'] - 0.5) > 0.4 else 
                                   "Medium" if abs(result['fraud_probability'] - 0.5) > 0.2 else "Low"
            }
            
            return result['verdict'], explanation
            
        except Exception as e:
            logger.error("❌ Error during transaction evaluation")
            logger.error(traceback.format_exc())
            raise e
    
    def _get_top_contributing_factors(self, transaction: Dict[str, Any], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Get the top features contributing to the prediction for this transaction.
        This is a simplified implementation and would ideally use SHAP values or similar.
        
        Args:
            transaction: Dictionary containing transaction data
            top_n: Number of top factors to return
            
        Returns:
            List of dictionaries with feature names and their contributions
        """
        # This is a simplified implementation - a production system would use
        # more sophisticated methods like SHAP values
        if not hasattr(self.model, 'feature_importances_'):
            return []
            
        # Get global feature importance
        importance = self.get_feature_importance()
        
        # Create transaction DataFrame
        transaction_df = pd.DataFrame([transaction])
        if 'transaction_id' in transaction_df.columns:
            transaction_df = transaction_df.drop('transaction_id', axis=1)
            
        # Process it like normal prediction
        processed_df = self.preprocess_data(transaction_df)
        
        # Get feature values and importance
        factors = []
        for feature in self.expected_features:
            if feature in processed_df.columns:
                value = float(processed_df[feature].iloc[0])
                # Combine global importance with feature value (absolute deviation from mean)
                # This is a simple heuristic - real implementation would use SHAP or similar
                contribution = abs(value) * importance.get(feature, 0)
                factors.append({
                    'feature': feature,
                    'value': value,
                    'contribution': contribution
                })
        
        # Sort by contribution and return top N
        factors.sort(key=lambda x: x['contribution'], reverse=True)
        return factors[:top_n]


if __name__ == "__main__":
    try:
        print("\n" + "="*50)
        print("🔍 CREDIT CARD FRAUD DETECTION SYSTEM")
        print("="*50 + "\n")
        
        # Initialize detector
        detector = FraudDetector("model/fraud_model.pkl", "model/scaler.pkl")
        
        # Sample transaction (same structure as in your original example)
        sample_data = pd.DataFrame({
            "Amount": [250.0],
            "V1": [1.1], "V2": [-0.9], "V3": [0.3], "V4": [-1.2], "V5": [0.1],
            "V6": [0.5], "V7": [-0.7], "V8": [0.2], "V9": [0.4], "V10": [-0.2],
            "V11": [1.3], "V12": [-0.3], "V13": [0.8], "V14": [-1.1], "V15": [0.6],
            "V16": [0.7], "V17": [-0.5], "V18": [0.9], "V19": [-0.4], "V20": [0.2],
            "V21": [0.1], "V22": [0.3], "V23": [-0.8], "V24": [0.6], "V25": [0.7],
            "V26": [0.5], "V27": [-0.3], "V28": [0.4]
        })
        
        # For demonstration, assign a transaction ID
        sample_data['transaction_id'] = ['TX' + str(np.random.randint(10000, 99999))]
        
        print(f"Processing transaction: {sample_data['transaction_id'].iloc[0]}")
        print("-"*50)
        
        # Get and print detection result
        result = detector.detect_fraud(sample_data)
        
        print("\n📊 DETECTION RESULTS:")
        print(f"Transaction ID: {result['transaction_id']}")
        print(f"Verdict: {result['verdict']}")
        print(f"Fraud Probability: {result['fraud_probability']:.4f}")
        print(f"Timestamp: {result['timestamp']}")
        
        # Print feature importance if available
        feature_importance = detector.get_feature_importance()
        if feature_importance:
            print("\n🔑 TOP IMPORTANT FEATURES:")
            sorted_importance = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
            for feature, importance in sorted_importance[:5]:
                print(f"- {feature}: {importance:.4f}")
        
        print("\n" + "="*50)
        print("✅ Detection process completed successfully!")
        print("="*50)
        
    except Exception as e:
        logger.critical("🔥 Critical failure in fraud detection script")
        logger.critical(traceback.format_exc())
        print("\n❌ ERROR: Detection process failed. Check logs for details.")