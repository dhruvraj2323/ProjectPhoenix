"""
=================================================
Project Phoenix
Position Manager
M54
=================================================
"""

from __future__ import annotations

from uuid import uuid4

from paper_trading.paper_context import (
    PaperContext,
)

from paper_trading.paper_models import (
    PaperPosition,
    PositionStatus,
)


class PositionManager:
    """
    Creates and manages
    paper trading positions.
    """

    # --------------------------------------------------
    # Open Position
    # --------------------------------------------------

    def open_position(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Create paper position
        from paper order.
        """

        if context.order is None:

            return context

        position = PaperPosition(

            position_id=(
                self._generate_position_id()
            ),

            order_id=(
                context.order.order_id
            ),

            symbol=(
                context.order.symbol
            ),

            direction=(
                context.order.direction
            ),

            volume=(
                context.order.volume
            ),

            entry_price=(
                context.order.entry_price
            ),

            current_price=(
                context.market_price
            ),

            stop_loss=(
                context.order.stop_loss
            ),

            take_profit=(
                context.order.take_profit
            ),

            status=(
                PositionStatus.OPEN
            ),

        )

        context.position = position

        return context

    # --------------------------------------------------
    # Generate Position ID
    # --------------------------------------------------

    def _generate_position_id(
        self,
    ) -> str:
        """
        Generate unique paper
        position ID.
        """

        return (
            f"POSITION-{uuid4().hex[:12].upper()}"
        )

    # --------------------------------------------------
    # Update Context
    # --------------------------------------------------

    def update_context(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Synchronize position into
        PaperContext.
        """

        if context.position is not None:

            context.result.position = (
                context.position
            )

            context.statistics.total_positions += 1

            context.set_metadata(
                "position_id",
                context.position.position_id,
            )

            context.set_metadata(
                "position_status",
                context.position.status.value,
            )

        return context        