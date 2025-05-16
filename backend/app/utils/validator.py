import pandas as pd
from typing import List
from backend.app.config import Config
from backend.app.utils.logger import get_logger

logger = get_logger("Validator")

def validate_dataframe(df: pd.DataFrame, filename: str) -> None:
    """
    Validates the structure and contents of a dataset based on filename.
    """
    logger.info(f"🔎 Validating dataframe from file: {filename}")

    if df.empty:
        raise ValueError(f"The dataset from '{filename}' is empty.")

    # Fetch expected schema for the file
    required_columns: List[str] = Config.REQUIRED_COLUMNS.get(filename)
    if required_columns is None:
        raise ValueError(f"No schema defined in config for file: {filename}")

    # Check missing columns
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in '{filename}': {missing}")

    # Log null counts
    for col in required_columns:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            logger.warning(f"⚠️ Column '{col}' in '{filename}' contains {null_count} nulls")

    # Check target column
    target_col = Config.TARGET_COLUMN
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in '{filename}'.")

    unique_vals = df[target_col].dropna().unique()
    if not set(unique_vals).issubset({0, 1}):
        raise ValueError(f"Target column '{target_col}' must be binary (0/1), found in '{filename}': {unique_vals}")

    logger.info(f"✅ Validation successful for file: {filename}")