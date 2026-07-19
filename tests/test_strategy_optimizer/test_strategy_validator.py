"""
Project Phoenix

Unit Test
Strategy Validator
"""

from strategy_optimizer.strategy_models import (
    OptimizationRecommendation,
    OptimizationType,
)
from strategy_optimizer.strategy_validator import (
    StrategyValidator,
)


def test_strategy_validator():

    validator = StrategyValidator()

    recommendation = OptimizationRecommendation(
        optimization_type=OptimizationType.RISK_PERCENT,
        current_value=1.0,
        suggested_value=0.5,
        reason="Unit Test",
        confidence=0.90,
    )

    result = validator.validate(
        recommendation
    )

    print("===== Strategy Validator =====")
    print(f"Valid  : {result.valid}")
    print(f"Reason : {result.reason}")

    assert result.valid is True

    print()
    print("Strategy Validator Test Passed")


if __name__ == "__main__":

    test_strategy_validator()