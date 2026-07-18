"""
Test for risk_validator.py
"""

from risk.risk_models import (
    PositionSize,
    RiskDecision,
    StopLoss,
    TakeProfit,
    TradeDecision,
)
from risk.risk_validator import RiskValidator


decision = RiskDecision(
    decision=TradeDecision.APPROVE,
    position=PositionSize(
        quantity=100,
        capital_allocated=1000,
        risk_percent=1.0,
    ),
    stop_loss=StopLoss(
        price=245.0,
        reason="Test stop-loss",
    ),
    take_profit=TakeProfit(
        price=260.0,
        risk_reward_ratio=2.0,
    ),
    approved=True,
    reason="Risk validation passed.",
)

validator = RiskValidator()

result = validator.validate(decision)

print("===== Risk Validator Test =====")
print(f"Approved : {decision.approved}")
print(f"Valid    : {result}")
print(f"Reason   : {decision.reason}")