"""
=================================================
Project Phoenix
MT5 Connector
M55
=================================================
"""

from __future__ import annotations

from live_trading.live_models import (
    LiveExecutionResult,
)


class MT5Connector:
    """
    MT5 Connector Interface.

    V1.0 uses a simulated broker response.

    Real MT5 API integration
    will be added later.
    """

    def connect(
        self,
    ) -> bool:
        """
        Simulate MT5 connection.
        """

        return True

    def disconnect(
        self,
    ) -> None:
        """
        Simulate disconnect.
        """

        return None

    def send_order(
        self,
    ) -> LiveExecutionResult:
        """
        Simulate order execution.
        """

        return LiveExecutionResult(
            success=True,
            broker_ticket="SIM-100001",
            retcode=0,
            message="Order Executed",
            filled_price=0.0,
            filled_volume=0.0,
        )