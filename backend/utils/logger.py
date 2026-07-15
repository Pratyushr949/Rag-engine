import logging
import sys
from config.settings import settings

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with the specified name.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(settings.LOG_LEVEL)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger
