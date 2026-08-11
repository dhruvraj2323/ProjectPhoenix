"""
=================================================
Project Phoenix
Trade Request Builder
M59.7.6
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
    validated Risk Engine output.
    """

    def build(
        self,
        context: TradeContext,
    ) -> TradeRequest:

        signal = (
            context.strategy_result.signals[0]
        )

        # -----------------------------------------
        # Trade Direction
        # -----------------------------------------

        side = (

            OrderSide.BUY

            if signal.direction.value == "BUY"

            else OrderSide.SELL

        )

        # -----------------------------------------
        # Position Size
        # -----------------------------------------

        volume = (
            context.risk_result.metrics.position_size
        )

        # -----------------------------------------
        # Entry
        # -----------------------------------------

        entry_price = (
            signal.entry_price
        )

        # -----------------------------------------
        # Dynamic Risk Values
        # -----------------------------------------

        stop_loss = (
            context.risk_result.metrics.stop_loss
        )

        take_profit = (
            context.risk_result.metrics.take_profit
        )

        # -----------------------------------------
        # Build Request
        # -----------------------------------------

        request = TradeRequest(

            symbol=context.symbol,

            volume=volume,

            side=side,

            execution_type=ExecutionType.MARKET,

            price=entry_price,

            stop_loss=stop_loss,

            take_profit=take_profit,

        )

        # -----------------------------------------
        # Store
        # -----------------------------------------

        print()

        print("===== TRADE REQUEST =====")

        print(
            f"Entry : {request.price}"
        )

        print(
            f"SL    : {request.stop_loss}"
        )

        print(
            f"TP    : {request.take_profit}"
        )

        print("=========================")
        
        context.trade_request = request

        return request