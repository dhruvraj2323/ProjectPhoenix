"""
=================================================
Project Phoenix
Main Application
=================================================
"""

from core.config import config
from core.logger import logger


def main():
    """
    Application entry point.
    """

    app_logger = logger.initialize()

    config.load_environment()
    config.load_settings()
    config.validate()

    app_logger.info("Project Phoenix started successfully.")

    app_logger.info(
        f"Project: {config.settings['project']['name']}"
    )

    app_logger.info(
        f"Version: {config.settings['project']['version']}"
    )

    app_logger.info(
        f"Symbol: {config.settings['market']['symbol']}"
    )

    app_logger.info(
        f"Timeframe: {config.settings['market']['timeframe']}"
    )


if __name__ == "__main__":
    main()