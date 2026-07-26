"""
Project Phoenix
Milestone M9 - Risk Management Engine

Module:
    risk_position.py

Purpose:
    Calculates position sizing for approved trading signals.
"""

from __future__ import annotations

from risk.risk_models import PositionSize


class PositionSizer:
    """
    Calculates the position size based on account balance
    and risk percentage.
    """

    def calculate(
        self,
        account_balance: float,
        risk_percent: float = 1.0,
    ) -> PositionSize:
        """
        Calculate position size.

        Returns:
            PositionSize
        """

        if account_balance <= 0:
            raise ValueError("Account balance must be greater than zero.")

        if not (0.0 < risk_percent <= 100.0):
            raise ValueError("Risk percent must be between 0 and 100.")

        capital = account_balance * (risk_percent / 100.0)

        quantity = round(capital, 2)

        return PositionSize(
            quantity=quantity,
            capital_allocated=capital,
            risk_percent=risk_percent,
        )