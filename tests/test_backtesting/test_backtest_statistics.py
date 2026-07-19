"""
Project Phoenix

Unit Test
Backtest Statistics
"""

from backtesting.backtest_models import (
    BacktestContext,
)

from backtesting.backtest_simulator import (
    BacktestSimulator,
)

from backtesting.backtest_statistics import (
    BacktestStatisticsCalculator,
)


def test_backtest_statistics():

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

    calculator = (
        BacktestStatisticsCalculator()
    )

    statistics = calculator.calculate(
        trades
    )

    print("===== Backtest Statistics =====")

    print(
        f"Trades        : {statistics.total_trades}"
    )

    print(
        f"Win Rate      : {statistics.win_rate:.2f}%"
    )

    print(
        f"Net Profit    : {statistics.net_profit}"
    )

    print(
        f"Profit Factor : {statistics.profit_factor:.2f}"
    )

    print(
        f"Expectancy    : {statistics.expectancy:.2f}"
    )

    assert statistics.total_trades == 3

    assert statistics.net_profit == 900.0

    print("\nBacktest Statistics Test Passed")


if __name__ == "__main__":

    test_backtest_statistics()