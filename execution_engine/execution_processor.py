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
    Creates execution orders from
    approved trading decisions.
    """

    def process(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:

        signal = context.strategy_result.signals[0]

        order = ExecutionOrder(

            strategy_id=signal.strategy_id,

            symbol=context.symbol,

            side=signal.direction.value,

            quantity=1.0,

            entry_price=signal.entry_price,

            stop_loss=signal.stop_loss,

            take_profit=signal.take_profit,

            risk_percent=signal.risk_percent,

        )

        context.order = order

        context.execution_result.accepted = True

        context.execution_result.status = (
            context.execution_result.status.ACCEPTED
        )

        context.execution_result.executed_price = (
            signal.entry_price
        )

        return context