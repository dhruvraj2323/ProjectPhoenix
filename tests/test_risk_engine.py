"""
Test for risk_engine.py
"""

from risk.risk_engine import RiskEngine
from risk.risk_models import RiskContext
from signals.signal_models import SignalType, TradingSignal

signal = TradingSignal(
    signal=SignalType.BUY,
    strength=0.8,
    confidence=0.9,
    reason="Test signal",
    metadata={
        "entry_price": 250.0,
    },
)

context = RiskContext(
    signal=signal,
    account_balance=100000,
    symbol="RELIANCE",
)

engine = RiskEngine()

decision = engine.evaluate(context)

print()
print("===== Risk Engine Test =====")
print(f"Decision : {decision.decision.value}")
print(f"Approved : {decision.approved}")
print(f"Reason   : {decision.reason}")