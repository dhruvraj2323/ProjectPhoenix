"""
=================================================
Project Phoenix
Signal Engine
M34
=================================================
"""

from __future__ import annotations

from signal_engine.signal_context import (
    SignalContext,
)
from signal_engine.signal_processor import (
    SignalProcessor,
)
from signal_engine.signal_validator import (
    SignalValidator,
)
from signal_engine.signal_logger import (
    SignalLogger,
)


class SignalEngine:
    """
    Executes the complete
    Signal Engine pipeline.
    """

    def __init__(self) -> None:

        self.processor = SignalProcessor()
        self.validator = SignalValidator()
        self.logger = SignalLogger()

    # ---------------------------------------------------------

    def run(
        self,
        context: SignalContext,
    ) -> SignalContext:
        """
        Execute complete Signal Engine.
        """

        self.logger.log_start(
            context
        )

        if not self.validator.validate(
            context
        ):

            context.reject(
                decision="SIGNAL_VALIDATION_FAILED",
                reason="Signal validation failed.",
            )

            self.logger.log_failure(
                context
            )

            return context

        context = self.processor.process(
            context
        )

        context.approve(
            decision="SIGNALS_GENERATED",
            reason="Signal generation completed successfully.",
        )

        self.logger.log_finish(
            context
        )

        return context