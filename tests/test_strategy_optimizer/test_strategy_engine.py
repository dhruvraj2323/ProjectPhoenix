"""
Project Phoenix

Unit Test
Strategy Engine
"""

from strategy_optimizer.strategy_engine import (
    StrategyEngine,
)
from strategy_optimizer.strategy_models import (
    StrategyContext,
    StrategyPerformance,
)


def test_strategy_engine():

    engine = StrategyEngine()

    performance = StrategyPerformance(
        total_trades=120,
        win_rate=45.0,
        average_profit=150.0,
        average_loss=-90.0,
        drawdown=6.0,
        profit_factor=1.30,
        sharpe_ratio=1.05,
    )

    context = StrategyContext(
        performance=performance,
        current_parameters={
            "risk_percent": 1.0,
        },
    )

    decision = engine.evaluate(
        context
    )

    print()
    print("===== Strategy Engine =====")
    print(
        f"Status   : {decision.status.value}"
    )
    print(
        f"Approved : {decision.approved}"
    )
    print(
        f"Reason   : {decision.reason}"
    )

    assert decision.approved is True

    print()
    print("Strategy Engine Test Passed")


if __name__ == "__main__":

    test_strategy_engine()