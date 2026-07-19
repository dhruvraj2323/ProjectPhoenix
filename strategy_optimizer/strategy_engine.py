"""
Project Phoenix
Milestone M13 - Strategy Optimizer Engine

Module:
    strategy_engine.py

Purpose:
    Coordinates the complete Strategy
    Optimizer Engine.
"""

from __future__ import annotations

from strategy_optimizer.strategy_analyzer import (
    StrategyAnalyzer,
)
from strategy_optimizer.strategy_logger import (
    StrategyLogger,
)
from strategy_optimizer.strategy_models import (
    OptimizationDecision,
    OptimizationStatus,
    StrategyContext,
)
from strategy_optimizer.strategy_optimizer import (
    StrategyOptimizer,
)
from strategy_optimizer.strategy_validator import (
    StrategyValidator,
)


class StrategyEngine:
    """
    Coordinates the complete Strategy
    Optimizer Engine.
    """

    def __init__(self) -> None:

        self.analyzer = StrategyAnalyzer()

        self.optimizer = StrategyOptimizer()

        self.validator = StrategyValidator()

        self.logger = StrategyLogger()

    def evaluate(
        self,
        context: StrategyContext,
    ) -> OptimizationDecision:
        """
        Execute complete optimization workflow.
        """

        performance = self.analyzer.analyze(
            context
        )

        recommendation = self.optimizer.optimize(
            performance
        )

        validation = self.validator.validate(
            recommendation
        )

        decision = OptimizationDecision(

            status=(
                OptimizationStatus.APPROVED
                if validation.valid
                else OptimizationStatus.REJECTED
            ),

            recommendation=recommendation,

            approved=validation.valid,

            reason=validation.reason,

        )

        self.logger.log(
            decision
        )

        return decision