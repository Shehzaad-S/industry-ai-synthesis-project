"""Centralized Logging Configuration"""

import logging
import os
import sys

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | "
    "%(name)s | %(message)s"
)


def configure_logging(level: int = logging.INFO, log_file: str = "logs/workflow.log") -> None:
    """
    Configure application logging safely to output to a file.
    Ensures directories exist and clears old notebook handlers.
    """
    root_logger = logging.getLogger()

    # Remove existing handlers in notebook kernel to avoid duplicate logs
    if root_logger.handlers:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

    # Ensure the logs directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    # Configure logging to write to a file instead of stdout
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt="%H:%M:%S",
        filename=log_file,     # Directs logs to specified file
        filemode="a"
    )


def get_logger(name: str) -> logging.Logger:
    """
    Create a named logger.
    """
    return logging.getLogger(name)
