"""
=================================================
Project Phoenix
Indicator Engine
M32
=================================================
"""

from __future__ import annotations

from indicator_engine.indicator_calculator import IndicatorCalculator
from indicator_engine.indicator_context import IndicatorContext
from indicator_engine.indicator_logger import IndicatorLogger
from indicator_engine.indicator_validator import IndicatorValidator


class IndicatorEngine:
    """
    Main Indicator Engine.

    Responsible for validating,
    calculating and storing
    indicator results.
    """

    def __init__(self) -> None:

        self.validator = IndicatorValidator()
        self.calculator = IndicatorCalculator()
        self.logger = IndicatorLogger()

    # ---------------------------------------------------------

    def run(
        self,
        context: IndicatorContext,
    ) -> IndicatorContext:
        """
        Execute Indicator Engine.
        """

        self.logger.log_start(context)

        # -----------------------------------------------------
        # Validation
        # -----------------------------------------------------

        if not self.validator.validate(context):

            context.reject(
                decision="INDICATOR_VALIDATION_FAILED",
                reason="Indicator validation failed.",
            )

            self.logger.log_error(
                context.reason,
            )

            return context

        # -----------------------------------------------------
        # Indicator Calculation
        # -----------------------------------------------------

        context.indicators = self.calculator.calculate_all(
            context.candles
        )

        for indicator in context.indicators.keys():

            self.logger.log_indicator(
                indicator
            )

        # -----------------------------------------------------
        # Success
        # -----------------------------------------------------

        context.approve(
            decision="INDICATORS_CALCULATED",
            reason="Indicators calculated successfully.",
        )

        self.logger.log_finish(
            context
        )

        return context