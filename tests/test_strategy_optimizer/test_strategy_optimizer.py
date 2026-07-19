"""
Project Phoenix

Unit Test
Strategy Optimizer
"""

from strategy_optimizer.strategy_optimizer import (
    StrategyOptimizer,
)
from strategy_optimizer.strategy_models import (
    OptimizationType,
    StrategyPerformance,
)


def test_strategy_optimizer():

    optimizer = StrategyOptimizer()

    performance = StrategyPerformance(
        total_trades=100,
        win_rate=45.0,
        average_profit=120.0,
        average_loss=-80.0,
        drawdown=8.0,
        profit_factor=1.20,
        sharpe_ratio=0.90,
    )

    recommendation = optimizer.optimize(
        performance
    )

    print("===== Strategy Optimizer =====")
    print(
        f"Optimization : {recommendation.optimization_type.value}"
    )
    print(
        f"Current Value: {recommendation.current_value}"
    )
    print(
        f"Suggested    : {recommendation.suggested_value}"
    )
    print(
        f"Confidence   : {recommendation.confidence}"
    )
    print(
        f"Reason       : {recommendation.reason}"
    )

    assert (
        recommendation.optimization_type
        == OptimizationType.RISK_PERCENT
    )

    assert recommendation.suggested_value == 0.5

    print()
    print("Strategy Optimizer Test Passed")


if __name__ == "__main__":

    test_strategy_optimizer()