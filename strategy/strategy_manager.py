"""
=================================================
Project Phoenix
Strategy Manager
M38
=================================================
"""

from __future__ import annotations

from strategy.strategy_context import (
    StrategyContext,
)

from strategy.strategy_engine import (
    StrategyEngine,
)


class StrategyManager:
    """
    High-level interface for
    Strategy Engine.
    """

    def __init__(self) -> None:

        self.engine = StrategyEngine()

    def execute(
        self,
        context: StrategyContext,
    ) -> StrategyContext:
        """
        Execute complete
        strategy evaluation.
        """

        return self.engine.run(
            context,
        )

    def evaluate(
        self,
        context: StrategyContext,
    ) -> StrategyContext:
        """
        Alias for execute().
        """

        return self.execute(
            context,
        )