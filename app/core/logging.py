import logging
import os
from pathlib import Path

def setup_logging():
    """Configure application logging."""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_format = os.getenv(
        "LOG_FORMAT",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        handlers=[
            logging.StreamHandler(),  # Console handler
            logging.FileHandler(  # File handler
                filename=log_dir / "app.log",
                encoding="utf-8"
            )
        ]
    )

    # Create logger
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {log_level}")
    
    return logger 