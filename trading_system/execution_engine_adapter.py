"""
=================================================
Project Phoenix
Execution Engine Adapter
M40.5
=================================================
"""

from __future__ import annotations

from trading_system.trading_context import TradingContext


class ExecutionEngineAdapter:
    """
    Adapter for Execution Engine.
    """

    def __init__(
        self,
        execution_engine,
    ) -> None:

        self.execution_engine = execution_engine

    def execute(
        self,
        context: TradingContext,
    ) -> TradingContext:
        """
        Execute Execution Engine.
        """

        result = self.execution_engine.execute(
            signal=context.signal,
            quantity=context.quantity,
        )

        context.order_id = result.get(
            "order_id",
            "",
        )

        context.execution_price = result.get(
            "execution_price",
            0.0,
        )

        return context