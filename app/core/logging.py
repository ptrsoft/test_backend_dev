import logging
import sys
from typing import Any, Dict

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
            logging.FileHandler("app.log"),
        ],
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name
    """
    return logging.getLogger(name)


def log_request(
    logger: logging.Logger,
    method: str,
    url: str,
    status_code: int,
    duration: float,
    **kwargs: Any,
) -> None:
    """
    Log HTTP request details
    """
    log_data: Dict[str, Any] = {
        "method": method,
        "url": url,
        "status_code": status_code,
        "duration": f"{duration:.2f}s",
        **kwargs,
    }
    
    if status_code >= 500:
        logger.error("Request failed", extra=log_data)
    elif status_code >= 400:
        logger.warning("Request failed", extra=log_data)
    else:
        logger.info("Request successful", extra=log_data) 