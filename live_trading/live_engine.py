"""
=================================================
Project Phoenix
Live Trading Engine
M55
=================================================
"""

from __future__ import annotations

from live_trading.live_context import LiveContext
from live_trading.live_logger import LiveLogger
from live_trading.live_validator import LiveValidator


class LiveTradingEngine:
    """
    Core Live Trading Engine.
    """

    def __init__(self) -> None:

        self.validator = LiveValidator()

        self.logger = LiveLogger()

    def run(
        self,
        context: LiveContext,
    ) -> LiveContext:
        """
        Execute Live Trading Engine.
        """

        if not self.validator.validate(context):

            context.fail("Live Trading validation failed.")

            self.logger.log_finish(context)

            return context

        context.complete()

        self.logger.log_finish(context)

        return context