from signals.signal_models import (
    SignalType,
    TradingSignal,
)

from risk.risk_models import (
    PositionSize,
    StopLoss,
    TakeProfit,
    RiskContext,
    RiskDecision,
    TradeDecision,
)


signal = TradingSignal(
    signal=SignalType.BUY,
    strength=0.80,
    confidence=90.0,
)

position = PositionSize(
    quantity=0.10,
    capital_allocated=1000.0,
    risk_percent=2.0,
)

stop_loss = StopLoss(
    price=1.0950,
    reason="ATR Stop",
)

take_profit = TakeProfit(
    price=1.1150,
    risk_reward_ratio=2.0,
)

context = RiskContext(
    signal=signal,
    account_balance=100000.0,
    symbol="EURUSD",
)

decision = RiskDecision(
    decision=TradeDecision.APPROVE,
    position=position,
    stop_loss=stop_loss,
    take_profit=take_profit,
    approved=True,
    reason="Risk checks passed.",
)

print("===== Risk Models Test =====")
print("Decision        :", decision.decision.value)
print("Approved        :", decision.approved)
print("Position Size   :", decision.position.quantity)
print("Stop Loss       :", decision.stop_loss.price)
print("Take Profit     :", decision.take_profit.price)
print("Risk %          :", decision.position.risk_percent)
print("Account Balance :", context.account_balance)
print("Symbol          :", context.symbol)