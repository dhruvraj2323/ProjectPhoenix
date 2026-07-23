"""
=================================================
Project Phoenix
Indicator Manager
M32
=================================================
"""

from __future__ import annotations

from indicator_engine.indicator_context import IndicatorContext
from indicator_engine.indicator_engine import IndicatorEngine


class IndicatorManager:
    """
    High-level manager for the Indicator Engine.

    Acts as the public interface used by
    Market Pipeline and future Trading Engine.
    """

    def __init__(self) -> None:

        self.engine = IndicatorEngine()

    # ---------------------------------------------------------

    def run(
        self,
        context: IndicatorContext,
    ) -> IndicatorContext:
        """
        Execute the complete Indicator Engine.
        """

        return self.engine.run(context)

    # ---------------------------------------------------------

    def calculate(
        self,
        context: IndicatorContext,
    ) -> IndicatorContext:
        """
        Alias for run().
        """

        return self.run(context)