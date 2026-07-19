"""
Project Phoenix

Unit Test
Strategy Models
"""

from strategy_optimizer.strategy_models import (
    OptimizationDecision,
    OptimizationRecommendation,
    OptimizationStatus,
    OptimizationType,
    StrategyContext,
    StrategyPerformance,
)


def test_strategy_models():

    performance = StrategyPerformance(
        total_trades=120,
        win_rate=62.5,
        average_profit=150.0,
        average_loss=-80.0,
        drawdown=4.2,
        profit_factor=1.85,
        sharpe_ratio=1.40,
    )

    recommendation = OptimizationRecommendation(
        optimization_type=OptimizationType.EMA_PERIOD,
        current_value=20,
        suggested_value=25,
        reason="Improve trend filtering.",
        confidence=0.91,
    )

    context = StrategyContext(
        performance=performance,
        current_parameters={
            "ema_period": 20,
        },
    )

    decision = OptimizationDecision(
        status=OptimizationStatus.APPROVED,
        recommendation=recommendation,
        approved=True,
        reason="Unit Test",
    )

    assert performance.total_trades == 120
    assert recommendation.suggested_value == 25
    assert context.current_parameters["ema_period"] == 20
    assert decision.approved is True

    print("Strategy Models Test Passed")


if __name__ == "__main__":

    test_strategy_models()