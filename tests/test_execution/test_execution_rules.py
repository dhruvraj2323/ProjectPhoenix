"""
Test for execution_rules.py
"""

from execution.execution_rules import ExecutionRules
from risk.risk_models import (
    PositionSize,
    RiskDecision,
    StopLoss,
    TakeProfit,
    TradeDecision,
)

decision = RiskDecision(
    decision=TradeDecision.APPROVE,
    position=PositionSize(
        quantity=0.10,
        capital_allocated=1000.0,
        risk_percent=1.0,
    ),
    stop_loss=StopLoss(
        price=3345.0,
        reason="Test stop-loss",
    ),
    take_profit=TakeProfit(
        price=3360.0,
        risk_reward_ratio=2.0,
    ),
    approved=True,
    reason="Risk approved.",
)

engine = ExecutionRules()

order = engine.create_order(decision)

print("===== Execution Rules Test =====")
print(f"Symbol      : {order.symbol}")
print(f"Side        : {order.side.value}")
print(f"Order Type  : {order.order_type.value}")
print(f"Volume      : {order.volume}")
print(f"Stop Loss   : {order.stop_loss}")
print(f"Take Profit : {order.take_profit}")
print(f"Comment     : {order.comment}")