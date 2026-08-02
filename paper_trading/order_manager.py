"""
=================================================
Project Phoenix
Order Manager
M54
=================================================
"""

from __future__ import annotations

from uuid import uuid4

from paper_trading.paper_context import (
    PaperContext,
)

from paper_trading.paper_models import (
    ExecutionMode,
    OrderStatus,
    OrderType,
    PaperOrder,
)


class OrderManager:
    """
    Creates and manages
    paper trading orders.
    """

    # --------------------------------------------------
    # Create Order
    # --------------------------------------------------

    def create_order(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Create new paper order.
        """

        order = PaperOrder(

            order_id=self._generate_order_id(),

            symbol=context.symbol,

            order_type=OrderType.MARKET,

            direction="BUY",

            volume=1.0,

            entry_price=context.market_price,

            stop_loss=0.0,

            take_profit=0.0,

            status=OrderStatus.CREATED,

            execution_mode=ExecutionMode.PAPER,

        )

        context.order = order

        return context

    # --------------------------------------------------
    # Generate Order ID
    # --------------------------------------------------

    def _generate_order_id(
        self,
    ) -> str:
        """
        Generate unique paper order ID.
        """

        return (
            f"PAPER-{uuid4().hex[:12].upper()}"
        )

    # --------------------------------------------------
    # Update Context
    # --------------------------------------------------

    def update_context(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Synchronize order into PaperContext.
        """

        if context.order is not None:

            context.result.order = (
                context.order
            )

            context.statistics.total_orders += 1

            context.set_metadata(
                "order_id",
                context.order.order_id,
            )

            context.set_metadata(
                "order_status",
                context.order.status.value,
            )

        return context        