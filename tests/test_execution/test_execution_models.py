"""
Test for execution_models.py
"""

from execution.execution_models import (
    ExecutionDecision,
    ExecutionStatus,
    OrderRequest,
    OrderSide,
    OrderType,
)

order = OrderRequest(
    symbol="XAUUSD",
    side=OrderSide.BUY,
    order_type=OrderType.MARKET,
    volume=0.10,
    entry_price=3350.00,
    stop_loss=3345.00,
    take_profit=3360.00,
)

decision = ExecutionDecision(
    status=ExecutionStatus.READY,
    order=order,
    approved=True,
    reason="Initial M10 placeholder execution.",
)

print("===== Execution Models Test =====")
print(f"Symbol      : {decision.order.symbol}")
print(f"Side        : {decision.order.side.value}")
print(f"Order Type  : {decision.order.order_type.value}")
print(f"Volume      : {decision.order.volume}")
print(f"Status      : {decision.status.value}")
print(f"Approved    : {decision.approved}")
print(f"Reason      : {decision.reason}")