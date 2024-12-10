import logging
from logging.handlers import RotatingFileHandler

# Configure logger
logger = logging.getLogger("AssignmentLogger")
logger.setLevel(logging.INFO)

# File handler for production logging
file_handler = RotatingFileHandler("assignment.log", maxBytes=5*1024*1024, backupCount=3)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Console handler for development
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)