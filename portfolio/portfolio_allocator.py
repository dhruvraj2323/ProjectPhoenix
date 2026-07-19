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
    ) -> AllocationInfo:
        """
        Allocate capital for a new position, respecting capital that
        is already committed to existing open positions.
        """

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
            * (allocation_percent / 100)
        )

        capital_used = min(
            requested_capital,
            remaining_capital,
        )

        capital_available = max(
            remaining_capital - capital_used,
            0.0,
        )

        return AllocationInfo(
            capital_used=capital_used,
            capital_available=capital_available,
            allocation_percent=allocation_percent,
            risk_used=risk_used,
            risk_available=100.0 - risk_used,
        )