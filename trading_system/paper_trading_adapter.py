"""
=================================================
Project Phoenix
Paper Trading Adapter
M40.6
=================================================
"""

from __future__ import annotations

from trading_system.trading_context import TradingContext


class PaperTradingAdapter:
    """
    Adapter for the Paper Trading Engine.
    """

    def __init__(
        self,
        paper_engine,
    ) -> None:

        self.paper_engine = paper_engine

    def execute(
        self,
        context: TradingContext,
    ) -> TradingContext:
        """
        Execute Paper Trading Engine.
        """

        result = self.paper_engine.execute(
            signal=context.signal,
            symbol=context.symbol,
            quantity=context.quantity,
        )

        context.paper_trade = result

        return context