"""
Project Phoenix
Milestone M12 - Portfolio Management Engine

Module:
    portfolio_correlation.py

Purpose:
    Calculates portfolio correlation risk based on how concentrated
    open positions are in the same symbol and direction.
"""

from __future__ import annotations

from portfolio.portfolio_models import (
    PortfolioContext,
)


class PortfolioCorrelation:
    """
    Calculates portfolio correlation risk.
    """

    def calculate(
        self,
        context: PortfolioContext,
    ) -> float:
        """
        Calculate correlation risk as a percentage (0-100).

        Positions in the same symbol AND same direction move together,
        so they are treated as highly correlated. The risk score is the
        percentage of total volume concentrated in the single largest
        symbol+direction group.

        Example:
            2 positions, both XAUUSD BUY -> 100.0 (fully correlated)
            2 positions, XAUUSD BUY + TCS SELL -> 50.0 (no overlap)
        """

        if len(context.positions) <= 1:
            return 0.0

        total_volume = sum(
            position.volume
            for position in context.positions
        )

        if total_volume <= 0:
            return 0.0

        group_volume = {}

        for position in context.positions:

            key = (position.symbol, position.direction)

            group_volume[key] = (
                group_volume.get(key, 0.0)
                + position.volume
            )

        largest_group_volume = max(group_volume.values())

        correlation_risk = (
            largest_group_volume / total_volume
        ) * 100.0

        return correlation_risk