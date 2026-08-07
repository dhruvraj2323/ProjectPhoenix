"""
=================================================
Project Phoenix
Demo Account Guard
M59.4.1
=================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5


class DemoAccountGuard:
    """
    Prevents Project Phoenix
    from trading on
    non-demo accounts.
    """

    def validate(
        self,
    ) -> bool:

        account = mt5.account_info()

        if account is None:

            raise RuntimeError(
                "MT5 account not available."
            )

        if account.trade_mode is None:

            raise RuntimeError(
                "Invalid account information."
            )

        # ------------------------------------------
        # MT5 Demo Account
        # trade_mode == 0
        # ------------------------------------------

        if account.trade_mode != 0:

            raise RuntimeError(
                "Live account detected. "
                "Trading aborted."
            )

        return True