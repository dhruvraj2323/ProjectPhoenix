"""
Project Phoenix
Milestone M12 - Portfolio Management Engine

Module:
    portfolio_allocator.py

Purpose:
    Calculates capital allocation for approved trades, taking into
    account capital already committed to existing open positions.
"""

from __future__ import annotations

from typing import List, Optional

from portfolio.portfolio_models import (
    AllocationInfo,
    PositionInfo,
)


class PortfolioAllocator:
    """
    Calculates portfolio capital allocation.
    """

    def allocate(
        self,
        total_capital: float,
        positions: Optional[List[PositionInfo]] = None,
        allocation_percent: float = 10.0,
        risk_used: float = 0.0,
        free_margin: Optional[float] = None,
    ) -> AllocationInfo:
        """
        Allocate capital for a new position.
        """

        if total_capital <= 0:
            raise ValueError(
                "Total capital must be greater than zero."
            )

        if not (0.0 < allocation_percent <= 100.0):
            raise ValueError(
                "Allocation percent must be between 0 and 100."
            )

        if not (0.0 <= risk_used <= 100.0):
            raise ValueError(
                "Risk used must be between 0 and 100."
            )

        positions = positions or []

        capital_already_used = sum(
            position.volume
            for position in positions
        )

        remaining_capital = max(
            total_capital - capital_already_used,
            0.0,
        )

        requested_capital = (
            total_capital
            * (allocation_percent / 100.0)
        )

        limits = [
            requested_capital,
            remaining_capital,
        ]

        if free_margin is not None:

            if free_margin < 0:
                raise ValueError(
                    "Free margin cannot be negative."
                )

            limits.append(free_margin)

        capital_used = min(limits)

        capital_available = max(
            remaining_capital - capital_used,
            0.0,
        )

        return AllocationInfo(
            capital_used=round(capital_used, 2),
            capital_available=round(capital_available, 2),
            allocation_percent=allocation_percent,
            risk_used=risk_used,
            risk_available=round(100.0 - risk_used, 2),
        )