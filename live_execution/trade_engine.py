"""
=================================================
Project Phoenix
Trade Engine
M59.1.8
=================================================
"""

from __future__ import annotations

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_executor import (
    TradeExecutor,
)

from live_execution.trade_logger import (
    TradeLogger,
)

from live_execution.trade_request_builder import (
    TradeRequestBuilder,
)

from live_execution.trade_validator import (
    TradeValidator,
)


class TradeEngine:
    """
    Complete Live Trade Engine.

    Pipeline

        Validate
            ↓
        Build Request
            ↓
        Execute Trade
            ↓
        Log Response
    """

    def __init__(
        self,
    ) -> None:

        self.validator = TradeValidator()

        self.builder = TradeRequestBuilder()

        self.executor = TradeExecutor()

        self.logger = TradeLogger()

    # --------------------------------------------------

    def run(
        self,
        context: TradeContext,
    ) -> TradeContext:
        """
        Execute complete
        Live Trade pipeline.
        """

        if not self.validator.validate(
            context,
        ):

            self.logger.log_error(
                context.reason,
            )

            return context

        self.builder.build(
            context,
        )

        self.logger.log_request(
            context,
        )

        self.executor.execute(
            context,
        )

        self.logger.log_response(
            context,
        )

        return context