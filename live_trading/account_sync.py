"""
=================================================
Project Phoenix
Account Sync
M55
=================================================
"""

from __future__ import annotations

from live_trading.live_context import LiveContext


class AccountSync:
    """
    Synchronizes the trading account.
    """

    def sync(
        self,
        context: LiveContext,
    ) -> None:
        """
        Simulate account synchronization.
        """

        account = context.account

        # Ensure valid defaults only when values
        # are not already provided.

        if account.balance <= 0:
            account.balance = 100000.0

        if account.equity <= 0:
            account.equity = account.balance

        if account.margin < 0:
            account.margin = 0.0

        if account.free_margin <= 0:
            account.free_margin = (
                account.equity - account.margin
            )

        if account.margin_level < 0:
            account.margin_level = 0.0

        if not account.currency:
            account.currency = "USD"

        if account.leverage <= 0:
            account.leverage = 100.0