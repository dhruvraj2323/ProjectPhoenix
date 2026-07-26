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
    Calculates the take-profit level using
    a configurable Risk:Reward ratio.
    """

    def calculate(
        self,
        entry_price: float,
        stop_loss_price: float,
        risk_reward_ratio: float = 2.0,
    ) -> TakeProfit:
        """
        Calculate take-profit price.

        Returns:
            TakeProfit
        """

        if entry_price <= 0:
            raise ValueError("Entry price must be greater than zero.")

        if stop_loss_price <= 0:
            raise ValueError("Stop-loss price must be greater than zero.")

        if stop_loss_price >= entry_price:
            raise ValueError(
                "Stop-loss price must be below entry price."
            )

        if risk_reward_ratio <= 0:
            raise ValueError(
                "Risk-reward ratio must be greater than zero."
            )

        risk = entry_price - stop_loss_price

        take_profit_price = round(
            entry_price + (risk * risk_reward_ratio),
            5,
        )

        return TakeProfit(
            price=take_profit_price,
            risk_reward_ratio=risk_reward_ratio,
        )