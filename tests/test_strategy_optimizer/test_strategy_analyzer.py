"""
Project Phoenix

Unit Test
Strategy Analyzer
"""

from strategy_optimizer.strategy_analyzer import (
    StrategyAnalyzer,
)
from strategy_optimizer.strategy_models import (
    StrategyContext,
    StrategyPerformance,
)


def test_strategy_analyzer():

    analyzer = StrategyAnalyzer()

    performance = StrategyPerformance(
        total_trades=150,
        win_rate=61.0,
        average_profit=180.0,
        average_loss=-90.0,
        drawdown=3.5,
        profit_factor=1.92,
        sharpe_ratio=1.55,
    )

    context = StrategyContext(
        performance=performance,
        current_parameters={
            "ema_period": 20,
        },
    )

    result = analyzer.analyze(context)

    print("===== Strategy Analyzer =====")
    print(f"Trades        : {result.total_trades}")
    print(f"Win Rate      : {result.win_rate}%")
    print(f"Profit Factor : {result.profit_factor}")
    print(f"Drawdown      : {result.drawdown}%")

    assert result.total_trades == 150
    assert result.win_rate == 61.0
    assert result.profit_factor == 1.92

    print()
    print("Strategy Analyzer Test Passed")


if __name__ == "__main__":

    test_strategy_analyzer()