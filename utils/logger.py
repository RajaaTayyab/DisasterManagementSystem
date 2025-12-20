"""
Centralized logging configuration for the disaster management system.

This module ensures consistent, clean, and structured logging across
all agents, environment models, and simulation components.
"""

import logging
import sys


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure global logging settings.

    :param level: Logging verbosity level
    """
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s",
        datefmt="%H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Prevent duplicate handlers
    if not root_logger.handlers:
        root_logger.addHandler(handler)
