"""
=================================================
Project Phoenix
Position Monitor
M55
=================================================
"""

from __future__ import annotations

from live_trading.live_context import LiveContext
from live_trading.live_models import LivePosition


class PositionMonitor:
    """
    Monitors live positions.
    """

    def get_position(
        self,
        context: LiveContext,
    ) -> LivePosition | None:
        """
        Return the current
        live position.
        """

        return context.position