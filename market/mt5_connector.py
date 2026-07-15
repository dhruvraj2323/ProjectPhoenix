"""
=================================================
Project Phoenix
MT5 Connection Manager
=================================================

Responsible for:
- MetaTrader 5 initialization
- Terminal connection
- Login management
- Connection validation
- Account information
- Graceful shutdown
"""

import MetaTrader5 as mt5

from core.logger import logger

# -------------------------------------------------
# Shared Application Logger
# -------------------------------------------------

app_logger = logger.initialize()

# -------------------------------------------------
# MT5 Connection Manager
# -------------------------------------------------


class MT5Connection:
    """
    Handles all MetaTrader 5 connection operations.
    """

    def __init__(self):
        """Initialize MT5 connection manager."""

        self.connected = False
        self.authorized = False

    def initialize(self):
        """
        Initialize MetaTrader 5 terminal.
        """

        if mt5.initialize():
            self.connected = True

            app_logger.info(
                "MetaTrader 5 initialized successfully."
            )

            return True

        app_logger.error(
            f"MT5 initialization failed: {mt5.last_error()}"
        )

        return False

    def login(self, login, password, server):
        """
        Login to MetaTrader 5 account.
        """

        if not self.connected:

            app_logger.error(
                "MT5 terminal is not initialized."
            )

            return False

        if mt5.login(
            login=login,
            password=password,
            server=server
        ):

            self.authorized = True

            app_logger.info(
                "MT5 login successful."
            )

            return True

        app_logger.error(
            f"MT5 login failed: {mt5.last_error()}"
        )

        return False

    def is_connected(self):
        """
        Verify MT5 connection status.
        """

        return self.connected and self.authorized

    def get_account_info(self):
        """
        Retrieve MT5 account information.
        """

        if not self.is_connected():

            app_logger.error(
                "MT5 is not connected."
            )

            return None

        account = mt5.account_info()

        if account is None:

            app_logger.error(
                "Unable to retrieve account information."
            )

            return None

        return account

    def shutdown(self):
        """
        Shutdown MetaTrader 5 connection.
        """

        mt5.shutdown()

        self.connected = False
        self.authorized = False

        app_logger.info(
            "MetaTrader 5 connection closed."
        )