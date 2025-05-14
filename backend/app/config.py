import os

class Config:
    # General Configurations
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # Corrected ROOT_DIR
    DATA_DIR = os.path.join(ROOT_DIR, "data")  # Corrected to point to backend/data
    MODEL_DIR = os.path.join(ROOT_DIR, "models")
    LOG_FILE = os.path.join(ROOT_DIR, "logs", "fraud_detector.log")

    # Logging
    LOG_LEVEL = "INFO"

    # Data Validation Configurations
    REQUIRED_COLUMNS = {
        "creditcard_2023.csv": ["Time", "V1", "V2", "V3", "V4", "Amount", "Class"],
        "creditcard.csv": ["Time", "V1", "V2", "V3", "V4", "Amount", "Class"],
        "PS_20174392719_1491204439457_log.csv": ["step", "type", "amount", "nameOrig", "oldbalanceOrg", "newbalanceOrig", "nameDest", "oldbalanceDest", "newbalanceDest", "isFraud"],
        # Add a generic schema for combined datasets
        "combined_dataset": ["Time", "V1", "V2", "V3", "V4", "Amount", "Class"]
    }
    TARGET_COLUMN = "Class"

    # Model Training Configurations
    TEST_SIZE = 0.2
    RANDOM_SEED = 42
    SMOTE_RANDOM_STATE = 42
    RF_N_ESTIMATORS = 100
    RF_CLASS_WEIGHT = "balanced"
    VERSION = "1.0.0"
    MODEL_PATH = os.path.join(MODEL_DIR, f"fraud_model_{VERSION}.pkl")
