"""
=================================================
Project Phoenix
Position Finder
M59.3.4
=================================================
"""

from __future__ import annotations

from live_execution.position_manager import (
    PositionManager,
)


class PositionFinder:
    """
    Finds MT5 positions.
    """

    def __init__(
        self,
    ) -> None:

        self.manager = PositionManager()

    def by_ticket(
        self,
        ticket: int,
    ):

        positions = (
            self.manager.get_positions()
        )

        if positions is None:

            return None

        for position in positions:

            if position.ticket == ticket:

                return position

        return None