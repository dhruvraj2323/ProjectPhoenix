"""
=================================================
Project Phoenix
Trade Request Builder
M59.1.4
=================================================
"""

from __future__ import annotations

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_models import (
    ExecutionType,
    OrderSide,
    TradeRequest,
)


class TradeRequestBuilder:
    """
    Builds a TradeRequest from
    the validated TradeContext.
    """

    def build(
        self,
        context: TradeContext,
    ) -> TradeRequest:

        side = OrderSide.BUY

        if hasattr(
            context.signal_result,
            "side",
        ):
            side = context.signal_result.side

        volume = 0.01

        if hasattr(
            context.risk_result,
            "position_size",
        ):
            volume = (
                context.risk_result.position_size
            )

        price = 0.0

        if hasattr(
            context.strategy_result,
            "entry_price",
        ):
            price = (
                context.strategy_result.entry_price
            )

        stop_loss = 0.0

        if hasattr(
            context.strategy_result,
            "stop_loss",
        ):
            stop_loss = (
                context.strategy_result.stop_loss
            )

        take_profit = 0.0

        if hasattr(
            context.strategy_result,
            "take_profit",
        ):
            take_profit = (
                context.strategy_result.take_profit
            )

        request = TradeRequest(

            symbol=context.symbol,

            volume=volume,

            side=side,

            execution_type=ExecutionType.MARKET,

            price=price,

            stop_loss=stop_loss,

            take_profit=take_profit,

        )

        context.trade_request = request

        return request