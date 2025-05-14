# Import Config and Logger Setup
from app.config import Config
from app.utils import get_logger

# Global logger setup
logger = get_logger(__name__)

# Initialize Config Object
config = Config()

# Log the app startup message
logger.info("App initialized with configuration settings")

# Optionally, you can set up additional setup or initialization steps if needed
# like database connections or cache systems

