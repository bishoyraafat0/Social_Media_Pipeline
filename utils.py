import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_env_vars():
    """Load API keys from .env file"""
    load_dotenv()
    env_vars = {
        'YT_API_KEY': os.getenv('YT_API_KEY'),
        'X_BEARER_TOKEN': os.getenv('X_BEARER_TOKEN')
    }
    for key, value in env_vars.items():
        if not value:
            logging.error(f"Missing environment variable: {key}")
            raise ValueError(f"Missing environment variable: {key}")
    return env_vars

def log_message(message, level='info'):
    """Log messages"""
    if level == 'info':
        logging.info(message)
    elif level == 'error':
        logging.error(message)
    elif level == 'warning':
        logging.warning(message)
