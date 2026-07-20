"""
Test for performance_metrics.py
"""

from performance.performance_metrics import PerformanceMetricsCalculator
from performance.performance_models import (
    PerformanceContext,
    TradeOutcome,
    TradeResult,
)


def test_performance_metrics_calculation():

    trades = [

        TradeResult(
            symbol="XAUUSD",
            outcome=TradeOutcome.WIN,
            profit_loss=150.0,
            entry_price=3350.0,
            exit_price=3365.0,
        ),

        TradeResult(
            symbol="XAUUSD",
            outcome=TradeOutcome.LOSS,
            profit_loss=-75.0,
            entry_price=3365.0,
            exit_price=3358.0,
        ),

        TradeResult(
            symbol="XAUUSD",
            outcome=TradeOutcome.WIN,
            profit_loss=100.0,
            entry_price=3370.0,
            exit_price=3380.0,
        ),
    ]


    context = PerformanceContext(
        trades=trades,
    )


    calculator = PerformanceMetricsCalculator()

    metrics = calculator.calculate(context)


    assert metrics.total_trades == 3
    assert metrics.wins == 2
    assert metrics.losses == 1
    assert metrics.breakeven == 0

    assert metrics.win_rate > 0
    assert metrics.average_profit == 125.0
    assert metrics.average_loss == -75.0