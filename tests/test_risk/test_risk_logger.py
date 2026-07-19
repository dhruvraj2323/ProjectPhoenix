"""
Test for risk_logger.py
"""

from risk.risk_logger import RiskLogger
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
        quantity=100,
        capital_allocated=1000,
        risk_percent=1.0,
    ),
    stop_loss=StopLoss(
        price=245.0,
        reason="Default stop-loss",
    ),
    take_profit=TakeProfit(
        price=260.0,
        risk_reward_ratio=2.0,
    ),
    approved=True,
    reason="Risk validation passed.",
)

logger = RiskLogger()

logger.log(decision)