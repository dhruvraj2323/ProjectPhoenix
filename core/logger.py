"""
=================================================
Project Phoenix
Central Logging System
=================================================

Responsible for:

- Console logging
- File logging
- Error logging
- Application logging
"""

import logging

from core.config import PROJECT_ROOT

# -------------------------------------------------
# Logger Manager
# -------------------------------------------------


class LoggerManager:
    """
    Central logging manager for Project Phoenix.
    """

    def __init__(self):
        """Initialize the logger manager."""
        self.logger = None

    def setup_console_logger(self):
        """
        Configure console logger.
        """

        self.logger = logging.getLogger("ProjectPhoenix")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:

            console_handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            console_handler.setFormatter(formatter)

            self.logger.addHandler(console_handler)

        return self.logger

    def setup_file_logger(self):
        """
        Configure file logger.
        """

        log_dir = PROJECT_ROOT / "logs"
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "project_phoenix.log"

        # Prevent duplicate file handlers
        file_exists = any(
            isinstance(handler, logging.FileHandler)
            for handler in self.logger.handlers
        )

        if not file_exists:

            file_handler = logging.FileHandler(
                log_file,
                encoding="utf-8"
            )

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

        return self.logger

    def initialize(self):
        """
        Initialize the complete logging system.
        """

        self.setup_console_logger()
        self.setup_file_logger()

        self.logger.info(
            "Logging system initialized successfully."
        )

        return self.logger


# -------------------------------------------------
# Global Logger Instance
# -------------------------------------------------

logger = LoggerManager()