import logging
from logging.handlers import RotatingFileHandler

# Set up logging configuration
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = "pipeline.log"

# Create a rotating file handler
handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)  # 5 MB per file, keep 5 backups
handler.setFormatter(log_formatter)

# Create a logger and set the level
logger = logging.getLogger("PipelineLogger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def log_error(message):
    """Logs errors during the pipeline processing."""
    logger.error(message)

def log_info(message):
    """Logs general information like performance."""
    logger.info(message)

def log_debug(message):
    """Logs debug information for detailed tracing."""
    logger.debug(message)

def log_warning(message):
    """Logs warnings that may indicate potential issues."""
    logger.warning(message)

def log_exception(exc):
    """Logs exceptions with a stack trace."""
    logger.exception("An exception occurred: %s", exc)
