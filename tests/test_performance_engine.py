"""
Test for performance_engine.py
"""

from performance.performance_engine import PerformanceEngine
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

engine = PerformanceEngine()

decision = engine.evaluate(context)

print()
print("===== Performance Engine Test =====")
print(f"Decision     : {decision.decision.value}")
print(f"Approved     : {decision.approved}")
print(f"Win Rate     : {decision.metrics.win_rate:.2f}%")
print(f"Reason       : {decision.reason}")