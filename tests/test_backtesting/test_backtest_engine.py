"""
Project Phoenix

Unit Test
Backtesting Engine
"""

from backtesting.backtest_models import (
    BacktestContext,
)

from backtesting.backtest_engine import (
    BacktestEngine,
)


def test_backtest_engine():

    context = BacktestContext(

        strategy_name="Phoenix Strategy",

        symbol="RELIANCE",

        timeframe="15m",

        initial_balance=100000.0,

    )

    engine = BacktestEngine()

    decision = engine.run(
        context
    )

    print("\n===== Backtest Engine =====")

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

    print("\nBacktest Engine Test Passed")


if __name__ == "__main__":

    test_backtest_engine()