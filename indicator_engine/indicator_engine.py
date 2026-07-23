"""
=================================================
Project Phoenix
Indicator Engine
M32
=================================================
"""

from __future__ import annotations

from indicator_engine.indicator_context import IndicatorContext
from indicator_engine.indicator_calculator import IndicatorCalculator
from indicator_engine.indicator_validator import IndicatorValidator
from indicator_engine.indicator_logger import IndicatorLogger


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

        if not self.validator.validate(context):

            self.logger.log_error(
                "Indicator validation failed."
            )

            return context

        context.indicators = self.calculator.calculate_all(
            context.candles
        )

        for indicator in context.indicators.keys():

            self.logger.log_indicator(
                indicator
            )

        self.logger.log_finish(
            context
        )

        return context