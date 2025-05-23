from pathlib import Path
import os

# === Core Configuration ===
BASE_DIR = Path(__file__).resolve().parent
API_VERSION = "1.3.0"
APP_ENV = os.getenv("APP_ENV", "production")  # changeable via environment variable

# === Path Configuration ===
PATHS = {
    "model": BASE_DIR / "model" / "fraud_model.pkl",
    "scaler": BASE_DIR / "model" / "scaler.pkl",
    "data": BASE_DIR / "data",
    "logs": BASE_DIR / "logs"
}

# === Fraud Detection Rules ===
RULES_CONFIG = {
    "amount_threshold": 10000,    # USD
    "hourly_limit": 5000,         # USD per hour
    "ml_threshold": 0.82,         # Probability threshold
    "allowed_countries": ["US", "CA", "GB", "DE", "FR"],
    "high_risk_countries": ["RU", "CN", "NG", "IR", "KP"],
    "geo_check": True,
    "device_check": True
}

# === Model Configuration ===
MODEL_CONFIG = {
    "expected_features": [
        "Time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10",
        "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19", "V20",
        "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount"
    ],
    "version": "1.3.0"
}

# === Security Configuration ===
SECURITY_CONFIG = {
    "cors_origins": [
        "http://localhost:3000",
        "http://127.0.0.1:3000",  # Replace with production frontend domain
    ],
    "rate_limits": {
        "api": "500/day",
        "auth": "20/hour"
    },
    "https_redirect": True,
    "content_security_policy": "default-src 'self'; script-src 'self'; object-src 'none'",
    "x_frame_options": "DENY",
    "x_content_type_options": "nosniff"
}
