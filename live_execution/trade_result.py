"""
=================================================
Project Phoenix
Trade Result
M59.1.5
=================================================
"""

from __future__ import annotations

from datetime import UTC, datetime

from live_execution.trade_models import (
    ExecutionStatus,
    TradeResponse,
)


class TradeResultBuilder:
    """
    Builds a Phoenix TradeResponse
    from broker execution results.
    """

    def success(
        self,
        ticket: int,
        price: float,
        volume: float,
        message: str,
        retcode: int = 0,
    ) -> TradeResponse:

        return TradeResponse(

            status=ExecutionStatus.EXECUTED,

            ticket=ticket,

            executed_price=price,

            executed_volume=volume,

            broker_message=message,

            execution_time=datetime.now(UTC),

            retcode=retcode,

        )

    def failure(
        self,
        message: str,
        retcode: int = -1,
    ) -> TradeResponse:

        return TradeResponse(

            status=ExecutionStatus.FAILED,

            broker_message=message,

            execution_time=datetime.now(UTC),

            retcode=retcode,

        )