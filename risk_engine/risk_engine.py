"""
=================================================
Project Phoenix
Risk Engine
M36
=================================================
"""

from __future__ import annotations

from risk_engine.risk_context import RiskContext
from risk_engine.risk_logger import RiskLogger
from risk_engine.risk_processor import RiskProcessor
from risk_engine.risk_validator import RiskValidator


class RiskEngine:
    """
    Executes the complete Risk Engine pipeline.
    """

    def __init__(self) -> None:

        self.processor = RiskProcessor()

        self.validator = RiskValidator()

        self.logger = RiskLogger()

    # ---------------------------------------------------------

    def run(
        self,
        context: RiskContext,
    ) -> RiskContext:
        """
        Execute complete Risk Engine.
        """

        self.logger.log_start(
            context,
        )

        # Initial validation

        if not self.validator.validate(
            context,
        ):

            self.logger.log_failure(
                context,
            )

            return context

        # Perform calculations

        context = self.processor.process(
            context,
        )

        # Final validation updates final decision
        # and marks context completed.

        self.validator.validate(
            context,
        )

        self.logger.log_finish(
            context,
        )

        return context