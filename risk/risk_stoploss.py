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
    """

    def calculate(
        self,
        entry_price: float,
        stop_loss_percent: float = 2.0,
    ) -> StopLoss:
        """
        Calculate stop-loss price.

        Returns:
            StopLoss
        """

        if entry_price <= 0:
            raise ValueError("Entry price must be greater than zero.")

        if not (0.0 < stop_loss_percent < 100.0):
            raise ValueError(
                "Stop-loss percent must be greater than 0 and less than 100."
            )

        stop_price = round(
            entry_price * (1 - stop_loss_percent / 100.0),
            5,
        )

        return StopLoss(
            price=stop_price,
            reason="Default percentage-based stop-loss.",
        )