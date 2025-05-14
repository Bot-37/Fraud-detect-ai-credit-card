import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from app.config import Config
from app.utils.logger import get_logger
from app.utils.validator import validate_dataframe

logger = get_logger("Preprocessing")

def preprocess_data(df: pd.DataFrame, dataset_name: str):
    """
    Preprocesses the input DataFrame:
    - Validates
    - Handles missing values
    - Scales numerical features
    - Returns X, y, and scaler info
    """
    logger.info("🔍 Starting preprocessing")

    # Skip schema validation for combined_dataset
    if dataset_name != "combined_dataset":
        try:
            validate_dataframe(df, dataset_name)
        except Exception as e:
            logger.error(f"❌ Validation failed: {e}")
            raise

    logger.info(f"📊 Initial shape: {df.shape}")

    # Handle missing values in critical columns
    critical_columns = Config.REQUIRED_COLUMNS.get(dataset_name, [])
    if Config.TARGET_COLUMN in df.columns:
        critical_columns.append(Config.TARGET_COLUMN)

    for col in critical_columns:
        if col in df.columns:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                logger.warning(f"⚠️ Column '{col}' contains {missing_count} nulls. Filling with median.")
                df[col] = df[col].fillna(df[col].median())

    # Drop rows where the target column is still missing
    if Config.TARGET_COLUMN in df.columns:
        missing_target_count = df[Config.TARGET_COLUMN].isnull().sum()
        if missing_target_count > 0:
            logger.warning(f"⚠️ Dropping {missing_target_count} rows with missing target values.")
        df.dropna(subset=[Config.TARGET_COLUMN], inplace=True)

    logger.info(f"🧹 After handling critical missing values: {df.shape}")

    # Separate features and target
    X = df.drop(columns=[Config.TARGET_COLUMN])
    y = df[Config.TARGET_COLUMN]

    # Handle missing values in all features
    logger.info("🔄 Imputing missing values for all features")
    imputer = SimpleImputer(strategy="median")  # For numerical columns, use median
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
    
    # Double-check for remaining NaN values
    if X_imputed.isnull().values.any():
        logger.error("❌ Imputation failed! Features still contain NaN values.")
        raise ValueError("Features still contain NaN values after imputation.")

    # Select only numeric features
    numeric_cols = X_imputed.select_dtypes(include=[np.number]).columns.tolist()
    X_numeric = X_imputed[numeric_cols]

    # Scale numeric features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_numeric)

    logger.info("⚙️ Features scaled successfully")

    # Collect scaling info for metadata
    scaler_info = {
        "mean": scaler.mean_.tolist(),
        "scale": scaler.scale_.tolist(),
        "features": numeric_cols
    }

    logger.info("✅ Preprocessing complete")
    return X_scaled, y.values, scaler_info