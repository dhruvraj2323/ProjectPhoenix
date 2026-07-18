"""
Project Phoenix
Milestone M9 - Risk Management Engine

Module:
    risk_takeprofit.py

Purpose:
    Calculates take-profit levels for trading signals.
"""

from __future__ import annotations

from risk.risk_models import TakeProfit


class TakeProfitCalculator:
    """
    Calculates the take-profit level.

    Current implementation uses a configurable
    Risk:Reward ratio.
    """

    def calculate(
        self,
        entry_price: float,
        stop_loss_price: float,
        risk_reward_ratio: float = 2.0,
    ) -> TakeProfit:
        """
        Calculate take-profit price.

        Placeholder:
        Take Profit = Entry + (Risk × RR Ratio)
        """

        risk = entry_price - stop_loss_price

        take_profit_price = entry_price + (risk * risk_reward_ratio)

        return TakeProfit(
            price=take_profit_price,
            risk_reward_ratio=risk_reward_ratio,
        )