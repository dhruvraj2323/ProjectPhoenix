"""
=================================================
Project Phoenix
Execution Processor
M37
=================================================
"""

from __future__ import annotations

from execution_engine.execution_context import (
    ExecutionContext,
)
from execution_engine.execution_models import (
    ExecutionOrder,
)


class ExecutionProcessor:
    """
    Builds executable orders from signals.
    """

    def process(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:

        context.order = ExecutionOrder(
            symbol=context.symbol,
            side=context.signal,
            quantity=context.quantity,
            price=context.price,
        )

        context.execution_result.accepted = True

        context.execution_result.status = "READY"

        context.execution_result.order_id = (
            context.execution_id
        )

        context.execution_result.executed_price = (
            context.price
        )

        context.completed = True

        return context