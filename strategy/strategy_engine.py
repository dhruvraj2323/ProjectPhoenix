"""
=================================================
Project Phoenix
Strategy Engine
M52
=================================================
"""

from __future__ import annotations

from strategy.strategy_context import (
    StrategyContext,
)

from strategy.strategy_logger import (
    StrategyLogger,
)

from strategy.strategy_rules import (
    StrategyRules,
)

from strategy.strategy_validator import (
    StrategyValidator,
)


class StrategyEngine:
    """
    Executes the complete
    Strategy Engine pipeline.

    M52 Pipeline

    Validate
        ↓
    Strategy Evaluation
        ↓
    Multi-Timeframe Intelligence
        ↓
    Finalize
    """

    def __init__(
        self,
    ) -> None:

        self.validator = (
            StrategyValidator()
        )

        self.rules = (
            StrategyRules()
        )

        self.logger = (
            StrategyLogger()
        )

    # --------------------------------------------------
    # Run Engine
    # --------------------------------------------------

    def run(
        self,
        context: StrategyContext,
    ) -> StrategyContext:
        """
        Execute complete
        Strategy Engine.
        """

        # ------------------------------------
        # Start
        # ------------------------------------

        self.logger.log_start(
            context,
        )

        # ------------------------------------
        # Validate
        # ------------------------------------

        if not self.validator.validate(
            context,
        ):

            self.logger.log_failure(
                context,
            )

            return context

        # ------------------------------------
        # Evaluate Strategies
        # ------------------------------------

        context = self.rules.evaluate_s01(
            context,
        )

        context = self.rules.evaluate_s02(
            context,
        )

        context = self.rules.evaluate_s03(
            context,
        )

        context = self.rules.evaluate_s04(
            context,
        )

        # ------------------------------------
        # Complete
        # ------------------------------------

        context.complete()

        # ------------------------------------
        # Finish
        # ------------------------------------

        self.logger.log_finish(
            context,
        )

        return context