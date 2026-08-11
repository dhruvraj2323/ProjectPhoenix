"""
=================================================
Project Phoenix
Trade Request Builder
M60.2.1
=================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5

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

    Strategy entry_price is an analytical/reference
    price only.

    For MARKET execution:

        BUY  -> current MT5 Ask
        SELL -> current MT5 Bid
    """

    def build(
        self,
        context: TradeContext,
    ) -> TradeRequest:

        # ==================================================
        # Validate Upstream Results
        # ==================================================

        if context.strategy_result is None:

            raise RuntimeError(
                "Strategy result missing."
            )

        if not context.strategy_result.signals:

            raise RuntimeError(
                "No strategy signals available."
            )

        if context.risk_result is None:

            raise RuntimeError(
                "Risk result missing."
            )

        # ==================================================
        # Select Signal
        # ==================================================

        signal = (
            context.strategy_result.signals[0]
        )

        # ==================================================
        # Trade Direction
        # ==================================================

        side = (

            OrderSide.BUY

            if signal.direction.value == "BUY"

            else OrderSide.SELL

        )

        # ==================================================
        # Position Size
        # ==================================================

        volume = (
            context.risk_result.metrics.position_size
        )

        # ==================================================
        # Resolve Current MT5 Market Price
        # ==================================================

        tick = mt5.symbol_info_tick(
            context.symbol,
        )

        if tick is None:

            raise RuntimeError(
                f"Unable to retrieve current MT5 tick "
                f"for {context.symbol}."
            )

        if side == OrderSide.BUY:

            market_price = float(
                tick.ask
            )

        else:

            market_price = float(
                tick.bid
            )

        if market_price <= 0:

            raise RuntimeError(
                f"Invalid current market price "
                f"for {context.symbol}: "
                f"{market_price}"
            )

        # ==================================================
        # Broker Price Precision
        # ==================================================

        symbol_info = mt5.symbol_info(
            context.symbol,
        )

        if symbol_info is None:

            raise RuntimeError(
                f"MT5 symbol information unavailable "
                f"for {context.symbol}."
            )

        digits = int(
            symbol_info.digits
        )

        market_price = round(
            market_price,
            digits,
        )

        # ==================================================
        # Dynamic Risk Values
        # ==================================================

        stop_loss = float(
            context.risk_result.metrics.stop_loss
        )

        take_profit = float(
            context.risk_result.metrics.take_profit
        )

        stop_loss = round(
            stop_loss,
            digits,
        )

        take_profit = round(
            take_profit,
            digits,
        )

        # ==================================================
        # Build Request
        # ==================================================

        request = TradeRequest(

            symbol=context.symbol,

            volume=volume,

            side=side,

            execution_type=ExecutionType.MARKET,

            price=market_price,

            stop_loss=stop_loss,

            take_profit=take_profit,

        )

        # ==================================================
        # Diagnostics
        # ==================================================

        print()

        print(
            "===== TRADE REQUEST ====="
        )

        print(
            f"Symbol      : {request.symbol}"
        )

        print(
            f"Side        : {request.side.value}"
        )

        print(
            f"Volume      : {request.volume}"
        )

        print(
            f"Market Price: {request.price}"
        )

        print(
            f"Signal Price: {signal.entry_price}"
        )

        print(
            f"SL          : {request.stop_loss}"
        )

        print(
            f"TP          : {request.take_profit}"
        )

        print(
            "========================="
        )

        # ==================================================
        # Store Request
        # ==================================================

        context.trade_request = request

        return request