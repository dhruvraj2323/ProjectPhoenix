"""
Project Phoenix

Unit Test
Strategy Logger
"""

from strategy_optimizer.strategy_logger import (
    StrategyLogger,
)
from strategy_optimizer.strategy_models import (
    OptimizationDecision,
    OptimizationRecommendation,
    OptimizationStatus,
    OptimizationType,
)


def test_strategy_logger():

    logger = StrategyLogger()

    recommendation = OptimizationRecommendation(
        optimization_type=OptimizationType.RISK_PERCENT,
        current_value=1.0,
        suggested_value=0.5,
        reason="Unit Test",
        confidence=0.90,
    )

    decision = OptimizationDecision(
        status=OptimizationStatus.APPROVED,
        recommendation=recommendation,
        approved=True,
        reason="Strategy validation passed.",
    )

    logger.log(decision)

    print()
    print("Strategy Logger Test Passed")


if __name__ == "__main__":

    test_strategy_logger()