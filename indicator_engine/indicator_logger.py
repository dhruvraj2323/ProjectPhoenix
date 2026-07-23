"""
=================================================
Project Phoenix
Indicator Logger
M32
=================================================
"""

from __future__ import annotations

import logging

from indicator_engine.indicator_context import IndicatorContext


class IndicatorLogger:
    """
    Handles logging for the Indicator Engine.
    """

    def __init__(self) -> None:

        self.logger = logging.getLogger("ProjectPhoenix.IndicatorEngine")

    # ---------------------------------------------------------

    def log_start(
        self,
        context: IndicatorContext,
    ) -> None:

        self.logger.info(
            "Indicator Engine Started | "
            "Symbol=%s Timeframe=%s",
            context.symbol,
            context.timeframe,
        )

    # ---------------------------------------------------------

    def log_indicator(
        self,
        indicator_name: str,
    ) -> None:

        self.logger.info(
            "Calculated Indicator : %s",
            indicator_name,
        )

    # ---------------------------------------------------------

    def log_finish(
        self,
        context: IndicatorContext,
    ) -> None:

        self.logger.info(
            "Indicator Engine Completed | "
            "Indicators=%d",
            len(context.indicators),
        )

    # ---------------------------------------------------------

    def log_error(
        self,
        message: str,
    ) -> None:

        self.logger.error(message)