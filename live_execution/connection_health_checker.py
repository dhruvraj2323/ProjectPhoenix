"""
=================================================
Project Phoenix
Connection Health Checker
M59.4.5
=================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5


class ConnectionHealthChecker:
    """
    Verifies that MT5 terminal
    is connected and healthy.
    """

    def validate(
        self,
    ) -> bool:

        terminal = mt5.terminal_info()

        if terminal is None:

            raise RuntimeError(
                "Unable to access MT5 terminal."
            )

        if not terminal.connected:

            raise RuntimeError(
                "MT5 terminal is disconnected."
            )

        return True