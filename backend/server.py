"""
Fraud Detection API Service
"""
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_talisman import Talisman
from pydantic import BaseModel, ValidationError, confloat, constr
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from backend.app.fraud_detector import (
    FraudDetectionSystem,
    TransactionRequest,
    FraudResponse
)
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=config.ALLOWED_ORIGINS)  # Restrict CORS to specific origins
Talisman(app, content_security_policy=config.CSP_POLICY)  # Security headers

# Rate Limiting Middleware
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

# Configuration
class AppConfig:
    BASE_DIR = Path(__file__).parent.resolve()
    MODEL_DIR = BASE_DIR / 'model'
    DATA_DIR = BASE_DIR / 'data'
    MODEL_FILE = MODEL_DIR / 'fraud_model.pkl'
    SCALER_FILE = MODEL_DIR / 'scaler.pkl'
    PORT = int(os.getenv('APP_PORT', '5000'))
    HOST = os.getenv('APP_HOST', '0.0.0.0')

# Input Validation Models
class TransactionRequestModel(BaseModel):
    card_id: constr(min_length=8, max_length=32)
    amount: confloat(gt=0)
    merchant_id: constr(min_length=4, max_length=24)
    timestamp: datetime
    location: Dict[str, Any]
    device_fingerprint: constr(min_length=8)
    metadata: Dict[str, Any] = {}

class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Dict[str, Any] = {}
    status_code: int = 500

# Global Systems Initialization
try:
    fds = FraudDetectionSystem(
        model_path=AppConfig.MODEL_FILE,
        scaler_path=AppConfig.SCALER_FILE,
        rules_config=config.RULES_CONFIG
    )
except FileNotFoundError as e:
    logger.critical(f"Failed to initialize fraud detection system: {str(e)}")
    raise RuntimeError("Critical system dependency missing") from e

# Helper Functions
def format_error_response(error_code: str, message: str, status_code: int = 400, **details) -> Dict:
    return ErrorResponse(
        error_code=error_code,
        message=message,
        details=details,
        status_code=status_code
    ).dict()

# API Endpoints
@app.route('/health', methods=['GET'])
@limiter.limit("10 per minute")  # Rate limit for health checks
def health_check():
    """Service health endpoint"""
    return jsonify({
        "status": "OK",
        "version": config.API_VERSION,
        "model_version": "1.0.0",  # Static version declared in fraud_detector.py
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/check-transaction', methods=['POST'])
@limiter.limit("20 per minute")  # Prevent abuse of fraud detection endpoint
def check_transaction():
    """Fraud detection endpoint with comprehensive validation"""
    # Log request metadata
    correlation_id = request.headers.get('X-Correlation-ID', 'none')
    logger.info(f"Transaction check request - CID: {correlation_id}")

    try:
        # Validate input with Pydantic
        tx_data = TransactionRequestModel(**request.get_json())
    except ValidationError as e:
        logger.warning(f"Validation error - CID: {correlation_id} - {str(e)}")
        return jsonify(format_error_response(
            "VALIDATION_ERROR",
            "Invalid transaction data",
            status_code=400,
            errors=e.errors()
        )), 400

    try:
        # Convert to domain object
        tx_request = TransactionRequest(**tx_data.dict())
        
        # Perform fraud analysis
        response: FraudResponse = fds.analyze_transaction(tx_request)
        
        # Log results without sensitive data
        logger.info(f"Fraud check completed - CID: {correlation_id} "
                     f"TX: {response.transaction_id} "
                     f"Score: {response.risk_score:.2f}")

        # Prepare response
        return jsonify({
            "transaction_id": response.transaction_id,
            "risk_score": np.round(response.risk_score, 4),
            "is_fraud": response.is_fraud,
            "reasons": response.reasons,
            "model_version": response.model_version,
            "timestamp": response.timestamp
        }), 200

    except Exception as e:
        logger.error(f"Processing error - CID: {correlation_id} - {str(e)}", 
                     exc_info=True)
        return jsonify(format_error_response(
            "PROCESSING_ERROR",
            "Transaction processing failed",
            correlation_id=correlation_id,
            status_code=500
        )), 500

# Security Middleware
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

if __name__ == '__main__':
    # Create required directories
    AppConfig.DATA_DIR.mkdir(exist_ok=True)
    
    # Start application
    logger.info(f"Starting fraud detection service version {config.API_VERSION}")
    app.run(
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        debug=False,
        threaded=True
    )