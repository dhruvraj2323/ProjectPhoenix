"""
=================================================
Project Phoenix
Main Application
=================================================
"""

import os

from core.config import config
from core.logger import logger
from market.mt5_connector import MT5Connection


def main():
    """
    Application entry point.
    """

    app_logger = logger.initialize()

    # -----------------------------------------
    # Load Configuration
    # -----------------------------------------

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

    # -----------------------------------------
    # MT5 Connection Test
    # -----------------------------------------

    mt5_connection = MT5Connection()

    if mt5_connection.initialize():

        login = int(os.getenv("MT5_LOGIN"))
        password = os.getenv("MT5_PASSWORD")
        server = os.getenv("MT5_SERVER")

        if mt5_connection.login(
            login,
            password,
            server
        ):

            account = mt5_connection.get_account_info()

            if account:

                app_logger.info(
                    f"Account : {account.login}"
                )

                app_logger.info(
                    f"Server  : {account.server}"
                )

                app_logger.info(
                    f"Balance : {account.balance}"
                )

                app_logger.info(
                    f"Equity  : {account.equity}"
                )

        mt5_connection.shutdown()


if __name__ == "__main__":
    main()