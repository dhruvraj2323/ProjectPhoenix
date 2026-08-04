"""
=================================================
Project Phoenix
MT5 Connector
M58
=================================================
"""

from __future__ import annotations

import json
from pathlib import Path

import MetaTrader5 as mt5

from live_trading.live_models import (
    LiveExecutionResult,
)


class MT5Connector:
    """
    MetaTrader 5 Connector.
    """

    def __init__(
        self,
    ) -> None:

        self.login = None

        self.password = None

        self.server = None

        self.connected = False

        self._load_credentials()

    # --------------------------------------------------
    # Load Credentials
    # --------------------------------------------------

    def _load_credentials(
        self,
    ) -> None:
        """
        Load MT5 credentials from
        config/mt5_credentials.json
        """

        credential_file = (
            Path("config")
            / "mt5_credentials.json"
        )

        if not credential_file.exists():

            raise FileNotFoundError(
                "config/mt5_credentials.json not found."
            )

        with credential_file.open(
            "r",
            encoding="utf-8",
        ) as file:

            credentials = json.load(file)

        self.login = int(
            credentials["login"]
        )

        self.password = credentials[
            "password"
        ]

        self.server = credentials[
            "server"
        ]

    # --------------------------------------------------
    # Connect
    # --------------------------------------------------

    def connect(
        self,
    ) -> bool:
        """
        Initialize MT5 terminal
        and authorize account.
        """

        terminal_path = (
            r"C:\Program Files\MetaTrader 5\terminal64.exe"
        )

        if not mt5.initialize(
            path=terminal_path,
            login=self.login,
            password=self.password,
            server=self.server,
        ):

            print(
                "MT5 initialize failed:",
                mt5.last_error(),
            )

            self.connected = False

            return False

        self.connected = True

        print(
            "MT5 Connected Successfully."
        )

        return True

    # --------------------------------------------------
    # Disconnect
    # --------------------------------------------------

    def disconnect(
        self,
    ) -> None:
        """
        Shutdown MT5.
        """

        mt5.shutdown()

        self.connected = False

    # --------------------------------------------------
    # Connection Status
    # --------------------------------------------------

    def is_connected(
        self,
    ) -> bool:
        """
        Connection status.
        """

        return self.connected

    # --------------------------------------------------
    # Account Information
    # --------------------------------------------------

    def get_account_info(
        self,
    ):
        """
        Return MT5 account info.
        """

        if not self.connected:

            return None

        return mt5.account_info()

    # --------------------------------------------------
    # Send Order
    # --------------------------------------------------

    def send_order(
        self,
    ) -> LiveExecutionResult:
        """
        Placeholder.

        Real order execution
        will be implemented
        during live deployment.
        """

        return LiveExecutionResult(
            success=True,
            broker_ticket="SIM-100001",
            retcode=0,
            message="Order Executed",
            filled_price=0.0,
            filled_volume=0.0,
        )