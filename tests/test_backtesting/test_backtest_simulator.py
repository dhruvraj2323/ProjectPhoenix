"""
Project Phoenix

Unit Test
Backtest Simulator
"""

from backtesting.backtest_models import (
    BacktestContext,
)

from backtesting.backtest_simulator import (
    BacktestSimulator,
)


def test_backtest_simulator():

    context = BacktestContext(

        strategy_name="Phoenix Strategy",

        symbol="RELIANCE",

        timeframe="15m",

        initial_balance=100000.0,

    )

    simulator = BacktestSimulator()

    trades = simulator.simulate(
        context
    )

    print("===== Backtest Simulator =====")

    for index, trade in enumerate(
        trades,
        start=1,
    ):

        print(

            f"Trade {index}"

            f" | Profit : {trade.profit}"

            f" | Win : {trade.win}"

        )

    assert len(trades) == 3

    assert trades[0].win is True

    assert trades[1].win is False

    print("\nBacktest Simulator Test Passed")


if __name__ == "__main__":

    test_backtest_simulator()