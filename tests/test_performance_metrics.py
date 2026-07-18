"""
Test for performance_metrics.py
"""

from performance.performance_metrics import PerformanceMetricsCalculator
from performance.performance_models import (
    PerformanceContext,
    TradeOutcome,
    TradeResult,
)

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

print("===== Performance Metrics Test =====")
print(f"Total Trades   : {metrics.total_trades}")
print(f"Wins           : {metrics.wins}")
print(f"Losses         : {metrics.losses}")
print(f"Breakeven      : {metrics.breakeven}")
print(f"Win Rate       : {metrics.win_rate:.2f}%")
print(f"Average Profit : {metrics.average_profit}")
print(f"Average Loss   : {metrics.average_loss}")