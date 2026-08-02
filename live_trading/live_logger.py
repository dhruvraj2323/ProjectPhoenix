"""
=================================================
Project Phoenix
Live Trading Logger
M55
=================================================

Logs live trading operations.
"""

from __future__ import annotations

from live_trading.live_context import LiveContext


class LiveLogger:
    """
    Live Trading Logger.
    """

    def log_start(
        self,
        context: LiveContext,
    ) -> None:

        print("===== Live Trading Started =====")

        print(f"Live ID        : {context.live_id}")
        print(f"Account ID     : {context.account_id}")
        print(f"Symbol         : {context.symbol}")
        print(f"Timeframe      : {context.timeframe}")
        print()

    def log_account(
        self,
        context: LiveContext,
    ) -> None:

        account = context.account

        print("===== Account =====")

        print(f"Balance        : {account.balance}")
        print(f"Equity         : {account.equity}")
        print(f"Margin         : {account.margin}")
        print(f"Free Margin    : {account.free_margin}")
        print(f"Leverage       : {account.leverage}")
        print()

    def log_order(
        self,
        context: LiveContext,
    ) -> None:

        if context.order is None:
            return

        order = context.order

        print("===== Order =====")

        print(f"Order ID       : {order.order_id}")
        print(f"Symbol         : {order.symbol}")
        print(f"Volume         : {order.volume}")
        print(f"Price          : {order.price}")
        print(f"Status         : {order.status}")
        print()

    def log_position(
        self,
        context: LiveContext,
    ) -> None:

        if context.position is None:
            return

        position = context.position

        print("===== Position =====")

        print(f"Position ID    : {position.position_id}")
        print(f"Profit         : {position.profit}")
        print()

    def log_finish(
        self,
        context: LiveContext,
    ) -> None:

        print("===== Live Trading Finished =====")

        print(f"Completed      : {context.completed}")
        print(f"Failed         : {context.failed}")
        print(f"Reason         : {context.reason}")
        print()