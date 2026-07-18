"""
Project Phoenix
Milestone M9 - Risk Management Engine

Module:
    risk_stoploss.py

Purpose:
    Calculates stop-loss levels for trading signals.
"""

from __future__ import annotations

from risk.risk_models import StopLoss


class StopLossCalculator:
    """
    Calculates the stop-loss level.

    Current implementation uses a simple placeholder
    percentage-based calculation.
    """

    def calculate(
        self,
        entry_price: float,
        stop_loss_percent: float = 2.0,
    ) -> StopLoss:
        """
        Calculate stop-loss price.

        Placeholder:
        Stop-loss = Entry Price - Percentage
        """

        stop_price = entry_price * (1 - stop_loss_percent / 100)

        return StopLoss(
            price=stop_price,
            reason="Default percentage-based stop-loss.",
        )