# Import Config and Logger Setup
from backend.app.config import Config
from backend.app.utils.logger import get_logger
from backend.app.model.fraud_detector import load_model, predict_fraud


# Global logger setup
logger = get_logger(__name__)

# Initialize Config Object
config = Config()

# Log the app startup message
logger.info("App initialized with configuration settings")

# Optionally, you can set up additional setup or initialization steps if needed
# like database connections or cache systems

