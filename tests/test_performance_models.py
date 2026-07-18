"""
Test for performance_models.py
"""

from performance.performance_models import (
    PerformanceDecision,
    PerformanceDecisionType,
    PerformanceMetrics,
    TradeOutcome,
    TradeResult,
)

trade = TradeResult(
    symbol="XAUUSD",
    outcome=TradeOutcome.WIN,
    profit_loss=150.0,
    entry_price=3350.0,
    exit_price=3365.0,
)

metrics = PerformanceMetrics(
    total_trades=10,
    wins=7,
    losses=2,
    breakeven=1,
    win_rate=70.0,
    average_profit=120.0,
    average_loss=-60.0,
)

decision = PerformanceDecision(
    decision=PerformanceDecisionType.ACCEPT,
    metrics=metrics,
    approved=True,
    reason="Initial M11 placeholder performance.",
)

print("===== Performance Models Test =====")
print(f"Symbol          : {trade.symbol}")
print(f"Outcome         : {trade.outcome.value}")
print(f"Profit/Loss     : {trade.profit_loss}")
print(f"Total Trades    : {metrics.total_trades}")
print(f"Win Rate        : {metrics.win_rate}%")
print(f"Decision        : {decision.decision.value}")
print(f"Approved        : {decision.approved}")
print(f"Reason          : {decision.reason}")