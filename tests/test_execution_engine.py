"""
Test for execution_engine.py
"""

from execution.execution_engine import ExecutionEngine
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

engine = ExecutionEngine()

result = engine.execute(decision)

print()
print("===== Execution Engine Test =====")
print(f"Status    : {result.status.value}")
print(f"Approved  : {result.approved}")
print(f"Reason    : {result.reason}")