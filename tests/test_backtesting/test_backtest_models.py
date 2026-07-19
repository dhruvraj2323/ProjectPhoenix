"""
Project Phoenix

Unit Test
Backtesting Models
"""

from backtesting.backtest_models import (
    BacktestContext,
    BacktestDecision,
    BacktestStatistics,
    BacktestStatus,
    BacktestTrade,
)


def test_backtest_models():

    trade = BacktestTrade(

        symbol="RELIANCE",

        entry_price=2500.0,

        exit_price=2550.0,

        volume=10.0,

        profit=500.0,

        win=True,

    )

    statistics = BacktestStatistics(

        total_trades=100,

        win_rate=62.0,

        net_profit=15250.0,

        profit_factor=1.85,

        max_drawdown=4.3,

        expectancy=152.5,

    )

    context = BacktestContext(

        strategy_name="Phoenix Strategy",

        symbol="RELIANCE",

        timeframe="15m",

        initial_balance=100000.0,

    )

    decision = BacktestDecision(

        status=BacktestStatus.APPROVED,

        statistics=statistics,

        approved=True,

        reason="Historical performance acceptable.",

    )

    assert trade.win is True

    assert statistics.total_trades == 100

    assert context.symbol == "RELIANCE"

    assert decision.approved is True

    print("Backtesting Models Test Passed")


if __name__ == "__main__":

    test_backtest_models()