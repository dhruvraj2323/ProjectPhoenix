"""
=================================================
Project Phoenix
Execution Processor
M59.2.1
=================================================
"""

from __future__ import annotations

from execution_engine.execution_context import (
    ExecutionContext,
)

from execution_engine.execution_models import (
    ExecutionOrder,
)

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_manager import (
    TradeManager,
)


class ExecutionProcessor:
    """
    Creates execution orders from
    approved trading decisions.

    Integrates the Live Trade
    Execution Engine.

    Responsibilities:
    - Select executable strategy signal
    - Create Phoenix ExecutionOrder
    - Create TradeContext
    - Execute through TradeManager
    - Propagate MT5 execution response
    - Update ExecutionResult
    """

    def __init__(
        self,
    ) -> None:

        self.trade_manager = (
            TradeManager()
        )

    # -------------------------------------------------
    # Process
    # -------------------------------------------------

    def process(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:

        # -------------------------------------------------
        # Defensive Validation
        # -------------------------------------------------

        if (
            context.strategy_result is None
            or
            not context.strategy_result.signals
        ):

            context.fail(
                reason="No executable strategy signals."
            )

            return context

        # -------------------------------------------------
        # Select First Executable Signal
        # -------------------------------------------------

        signal = (
            context.strategy_result.signals[0]
        )

        # -------------------------------------------------
        # Create Phoenix Execution Order
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Create Live Trade Context
        # -------------------------------------------------

        trade_context = TradeContext(

            execution_id=context.execution_id,

            symbol=context.symbol,

            timeframe=context.timeframe,

            strategy_result=context.strategy_result,

            signal_result=context.signal_result,

            risk_result=context.risk_result,

            ai_result=context.ai_result,
        )

        # -------------------------------------------------
        # Execute Live Trade
        # -------------------------------------------------

        trade_context = (
            self.trade_manager.execute(
                trade_context,
            )
        )

        # -------------------------------------------------
        # Handle Trade Failure
        # -------------------------------------------------

        if trade_context.failed:

            context.fail(
                trade_context.reason,
            )

            return context

        # -------------------------------------------------
        # Trade Response
        # -------------------------------------------------

        trade_response = (
            trade_context.trade_response
        )

        # -------------------------------------------------
        # Defensive Response Validation
        # -------------------------------------------------

        if trade_response is None:

            context.fail(
                "Trade execution returned no response."
            )

            return context

        # -------------------------------------------------
        # Update Execution Result
        # -------------------------------------------------

        context.execution_result.accepted = True

        context.execution_result.status = (
            context.execution_result.status.ACCEPTED
        )

        context.execution_result.executed_price = (
            signal.entry_price
        )

        # -------------------------------------------------
        # Propagate MT5 Ticket
        #
        # MT5:
        #     trade_response.ticket
        #
        # Phoenix:
        #     execution_result.order_id
        # -------------------------------------------------

        if trade_response.ticket is not None:

            context.execution_result.order_id = (
                str(
                    trade_response.ticket
                )
            )

        # -------------------------------------------------
        # Store Trade Response
        # -------------------------------------------------

        context.metadata[
            "trade_response"
        ] = trade_response

        # -------------------------------------------------
        # Store MT5 Ticket Separately
        # -------------------------------------------------

        context.metadata[
            "mt5_ticket"
        ] = trade_response.ticket

        return context