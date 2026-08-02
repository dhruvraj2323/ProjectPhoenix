"""
=================================================
Project Phoenix
Order Executor
M55
=================================================
"""

from __future__ import annotations

from live_trading.live_models import (
    LiveExecutionResult,
)
from live_trading.mt5_connector import (
    MT5Connector,
)


class OrderExecutor:
    """
    Executes orders through
    the broker connector.
    """

    def __init__(
        self,
    ) -> None:

        self.connector = MT5Connector()

    def execute(
        self,
    ) -> LiveExecutionResult:
        """
        Execute a broker order.
        """

        self.connector.connect()

        result = self.connector.send_order()

        self.connector.disconnect()

        return result