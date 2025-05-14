import logging

# Setup logger
logger = logging.getLogger("fraud_detector")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Example utility function: You can expand this with validation, etc.
def log_info(message: str):
    logger.info(message)

def log_error(message: str):
    logger.error(message)
