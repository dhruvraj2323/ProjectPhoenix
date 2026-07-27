"""
=================================================
Project Phoenix
Strategy Engine
M38
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
    """

    def __init__(self) -> None:

        self.rules = StrategyRules()

        self.validator = StrategyValidator()

        self.logger = StrategyLogger()

    def run(
        self,
        context: StrategyContext,
    ) -> StrategyContext:
        """
        Execute Strategy Engine.
        """

        self.logger.log_start(
            context,
        )

        if not self.validator.validate(
            context,
        ):

            self.logger.log_failure(
                context,
            )

            return context

        # ------------------------------------
        # Execute Frozen Strategies
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

        context.complete()

        self.logger.log_finish(
            context,
        )

        return context