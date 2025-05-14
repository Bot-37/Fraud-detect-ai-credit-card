import pandas as pd
from typing import List, Dict
import os
import logging
from logging.handlers import RotatingFileHandler
from app.config import Config


def get_logger(name: str) -> logging.Logger:
    """Create and configure a logger."""
    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL)

    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger

    # Ensure log directory exists
    os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)

    # Rotating file handler
    file_handler = RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(Config.LOG_LEVEL)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(Config.LOG_LEVEL)
    console_handler.setFormatter(file_formatter)
    logger.addHandler(console_handler)

    return logger
