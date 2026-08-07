"""
=================================================
Project Phoenix
Account Information
M59.3.8
=================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5


class AccountInfo:
    """
    Provides access to
    MT5 account information.
    """

    def get(self):

        return mt5.account_info()

    def balance(self) -> float:

        info = self.get()

        if info is None:

            return 0.0

        return float(info.balance)

    def equity(self) -> float:

        info = self.get()

        if info is None:

            return 0.0

        return float(info.equity)

    def free_margin(self) -> float:

        info = self.get()

        if info is None:

            return 0.0

        return float(info.margin_free)

    def leverage(self) -> int:

        info = self.get()

        if info is None:

            return 0

        return int(info.leverage)