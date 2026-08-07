"""
=================================================
Project Phoenix
Position History
M59.3.7
=================================================
"""

from __future__ import annotations

from datetime import datetime

import MetaTrader5 as mt5


class PositionHistory:
    """
    Retrieves historical
    trade information from MT5.
    """

    def get_history(
        self,
        date_from: datetime,
        date_to: datetime,
    ):

        return mt5.history_deals_get(
            date_from,
            date_to,
        )