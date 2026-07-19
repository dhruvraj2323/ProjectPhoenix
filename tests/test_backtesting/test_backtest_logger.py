"""
Project Phoenix

Unit Test
Backtest Logger
"""

from backtesting.backtest_models import (
    BacktestContext,
    BacktestDecision,
    BacktestStatus,
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

from backtesting.backtest_logger import (
    BacktestLogger,
)


def test_backtest_logger():

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

    statistics = (

        BacktestStatisticsCalculator()

        .calculate(
            trades
        )

    )

    validation = (

        BacktestValidator()

        .validate(
            statistics
        )

    )

    decision = BacktestDecision(

        status=(
            BacktestStatus.APPROVED
            if validation.valid
            else BacktestStatus.REJECTED
        ),

        statistics=statistics,

        approved=validation.valid,

        reason=validation.reason,

    )

    logger = BacktestLogger()

    logger.log(
        decision
    )

    print("\nBacktest Logger Test Passed")


if __name__ == "__main__":

    test_backtest_logger()