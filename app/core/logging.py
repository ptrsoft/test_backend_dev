import logging
import sys
from typing import Optional
from app.core.config import settings


def setup_logging() -> None:
    """
    Configure logging for the application
    """
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name
    """
    return logging.getLogger(name)


def log_request(
    logger: logging.Logger,
    method: str,
    url: str,
    status_code: int,
    duration: float,
    error: Optional[str] = None
) -> None:
    """
    Log HTTP request details
    """
    log_data = {
        "method": method,
        "url": url,
        "status_code": status_code,
        "duration": f"{duration:.3f}s"
    }
    
    if error:
        log_data["error"] = error
        logger.error(f"Request failed: {log_data}")
    else:
        logger.info(f"Request completed: {log_data}") 