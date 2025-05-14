import os
import json
import hashlib
import joblib
import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE

from app.utils.logger import get_logger
from app.utils.validator import validate_dataframe
from app.utils.preprocessing import preprocess_data
from app.config import Config

logger = get_logger("FraudTrainer")

def generate_model_hash(filepath: str) -> str:
    """Generate a SHA256 hash for the saved model file."""
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def evaluate_model(y_true, y_pred, y_prob):
    """Print and return classification report and AUC."""
    report = classification_report(y_true, y_pred, output_dict=True)
    auc = roc_auc_score(y_true, y_prob)
    logger.info("[Classification Report]\n" + classification_report(y_true, y_pred))
    logger.info(f"AUC Score: {auc:.4f}")
    return report, auc

def save_metadata(model_name: str, report: dict, auc_score: float, scaler_info: dict, hash_val: str):
    """Save model training metadata securely."""
    metadata = {
        "model_name": model_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "metrics": {
            "precision": report['1']['precision'],
            "recall": report['1']['recall'],
            "f1_score": report['1']['f1-score'],
            "roc_auc": auc_score
        },
        "scaler": scaler_info,
        "hash": hash_val
    }
    metadata_path = os.path.join(Config.MODEL_DIR, f"{model_name}_metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)
    logger.info(f"✅ Metadata saved at: {metadata_path}")

def load_all_csvs():
    """Load, validate, and combine all CSVs from /data."""
    logger.info("🔍 Loading and validating datasets from /data")
    dataframes = []

    for file in os.listdir(Config.DATA_DIR):
        if file.endswith(".csv"):
            path = os.path.join(Config.DATA_DIR, file)
            try:
                df = pd.read_csv(path)
                required_columns = Config.REQUIRED_COLUMNS.get(file)

                if required_columns:
                    # Add missing columns with NaN values
                    for col in required_columns:
                        if col not in df.columns:
                            logger.warning(f"⚠️ Column '{col}' missing in {file}. Filling with NaN.")
                            df[col] = pd.NA
                else:
                    logger.warning(f"⚠️ No schema defined for {file}. Skipping validation.")

                # Validate the dataset
                validate_dataframe(df, file)
                dataframes.append(df)
                logger.info(f"✅ Loaded {file} — shape: {df.shape}")
            except Exception as e:
                logger.warning(f"❌ Skipped {file}: {e}")

    if not dataframes:
        raise ValueError("No valid CSVs found in the data directory.")

    # Combine all datasets
    combined_df = pd.concat(dataframes, ignore_index=True)
    logger.info(f"📊 Combined dataset shape: {combined_df.shape}")
    return combined_df

def train_fraud_model():
    """Main training pipeline for the fraud detection model."""
    logger.info("🚀 Starting training pipeline")

    # Load and merge all valid datasets
    df = load_all_csvs()
    logger.info(f"📊 Combined dataset shape: {df.shape}")

    # Preprocess: feature scaling, encoding, etc.
    X, y, scaler_info = preprocess_data(df, "combined_dataset")

    # Train/Test split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, stratify=y, test_size=Config.TEST_SIZE, random_state=Config.RANDOM_SEED
    )

    # Handle class imbalance
    sm = SMOTE(random_state=Config.SMOTE_RANDOM_STATE)
    X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

    # Train model
    clf = RandomForestClassifier(
        n_estimators=Config.RF_N_ESTIMATORS,
        random_state=Config.RANDOM_SEED,
        class_weight=Config.RF_CLASS_WEIGHT
    )
    clf.fit(X_train_res, y_train_res)

    # Evaluation
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]
    report, auc_score = evaluate_model(y_test, y_pred, y_prob)

    # Save model
    model_filename = f"fraud_model_{Config.VERSION}.pkl"
    model_path = os.path.join(Config.MODEL_DIR, model_filename)
    joblib.dump(clf, model_path)
    logger.info(f"✅ Model saved at: {model_path}")

    # Save metadata
    model_hash = generate_model_hash(model_path)
    save_metadata(model_filename[:-4], report, auc_score, scaler_info, model_hash)

    logger.info("🎉 Training complete! Model & metadata saved securely.")

if __name__ == "__main__":
    train_fraud_model()