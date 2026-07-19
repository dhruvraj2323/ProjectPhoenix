"""
Project Phoenix

Unit Test
Backtest Validator
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

from backtesting.backtest_validator import (
    BacktestValidator,
)


def test_backtest_validator():

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

    validator = BacktestValidator()

    result = validator.validate(
        statistics
    )

    print("===== Backtest Validator =====")

    print(
        f"Valid  : {result.valid}"
    )

    print(
        f"Reason : {result.reason}"
    )

    assert result.valid is True

    print("\nBacktest Validator Test Passed")


if __name__ == "__main__":

    test_backtest_validator()